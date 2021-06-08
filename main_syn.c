#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define G 6.6743015151515151515151515151515e-11
#define dt 1000
#define INPUT_FILE "data.txt"
#define OUTPUT_FILE "output.txt"
#define NUM_ITER 100

int main(){
    FILE *f;
    ssize_t read;
    size_t len = 0;
    int i = 0;
    int id, rows, params;
    double mass, posx, posy, posz, velx, vely, velz;
    char* line = NULL;
    if ((f = fopen(INPUT_FILE,"r")) == NULL){
        printf("Error! opening file");
        exit(1);
   }
    fscanf(f, "%d", &rows);
    fscanf(f, "%d", &params);
    double data[(int)rows][(int)params];
    int ids[rows];

    while((read = getline(&line, &len, f)) != -1 && i < rows){
        fscanf(f, "%d", &id);
        fscanf(f, "%lf", &mass);
        fscanf(f, "%lf", &posx);
        fscanf(f, "%lf", &posy);
        fscanf(f, "%lf", &posz);
        fscanf(f, "%lf", &velx);
        fscanf(f, "%lf", &vely);
        fscanf(f, "%lf", &velz);
        
        ids[i] = id;
        data[i][0] = mass;
        data[i][1] = posx;
        data[i][2] = posy;
        data[i][3] = posz;
        data[i][4] = velx;
        data[i][5] = vely;
        data[i][6] = velz;
        i++;
    }
    fclose(f);
    if(line)    free(line);
    
    double** bodyAcceleration;
    bodyAcceleration = (double **)calloc(rows, sizeof(double*));
    for(int i = 0; i < rows; i++){
        bodyAcceleration[i] = (double *)calloc(3, sizeof(double));
    }

    struct timeval stop, start;
        gettimeofday(&start, NULL);

    for(int i = 0; i < NUM_ITER; i++){
        for(int k = 0; k < rows; k++){
            double mass = data[k][0];
            for(int j = 0; j < rows; j++){
                if(k == j) continue;

                double F = G*(data[k][0]*data[j][0] / sqrt(pow(data[k][1] - data[j][1], 2) + pow(data[k][2] - data[j][2], 2) + pow(data[k][2] - data[j][2], 2)));
                
                double wektor[3];
                wektor[0] = data[j][1] - data[k][1];
                wektor[1] = data[j][2] - data[k][2];
                wektor[2] = data[j][3] - data[k][3];
                double len = sqrt(fabs(pow(wektor[0],2) + pow(wektor[1], 2) + pow(wektor[2], 2)));
                double wersor[3];
                wersor[0] = wektor[0] / len;
                wersor[1] = wektor[1] / len;
                wersor[2] = wektor[2] / len;              

                bodyAcceleration[k][0] += F * wersor[0] / mass;
                bodyAcceleration[k][1] += F * wersor[1] / mass;
                bodyAcceleration[k][2] += F * wersor[2] / mass;
            }
        }

        for(int i = 0; i < rows; i++){
            data[i][1] += dt*data[i][4] + 0.5 * bodyAcceleration[i][0] * pow(dt,2); 
            data[i][2] += dt*data[i][5] + 0.5 * bodyAcceleration[i][1] * pow(dt,2);
            data[i][3] += dt*data[i][6] + 0.5 * bodyAcceleration[i][2] * pow(dt,2);
            data[i][4] += dt*bodyAcceleration[i][0];
            data[i][5] += dt*bodyAcceleration[i][1];
            data[i][6] += dt*bodyAcceleration[i][2];
        }
    }

    gettimeofday(&stop, NULL);
	    printf("Czas obliczen  %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec); 
       
    
    f = fopen(OUTPUT_FILE, "w");
    for(int i = 0; i < rows; i++){    
        fprintf(f, "%i %lf %lf %lf %lf %lf %lf %lf\n", ids[i], data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]);
    }   
    fclose(f);
    
    for(int i = 0; i<rows; i++){
        free(bodyAcceleration[i]); 
    }
    free(bodyAcceleration);
    
    exit(EXIT_SUCCESS);
}