#include <iostream>
#include <string.h>

int ip[64]={    58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17,  9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7
            };

int inverse_ip[64]={    40, 8, 48, 16, 56, 24, 64, 32,
                        39, 7, 47, 15, 55, 23, 63, 31,
                        38, 6, 46, 14, 54, 22 ,62, 30,
                        37, 5, 45, 13, 53, 21, 61, 29,
                        36, 4 ,44, 12, 52, 20, 60, 28,
                        35, 3, 43, 11, 51, 19, 59, 27,
                        34, 2 ,42, 10, 50, 18, 58, 26,
                        33, 1, 41,  9, 49 ,17, 57, 25
                    };


int e[48]={    32,  1,  2,  3,  4,  5,
                4,   5,  6,  7,  8,  9,
                8,   9, 10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21,
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1
            };

int pc_1[56]={     57, 49, 41, 33, 25, 17, 9,
                    1,  58, 50, 42, 34, 26, 18,
                    10, 2,  59, 51, 43, 35, 27,
                    19, 11, 3,  60, 52, 44, 36,
                    63, 55, 47, 39, 31, 23, 15,
                    7,  62, 54, 46, 38, 30, 22,
                    14, 6,  61, 53, 45, 37, 29,
                    21, 13, 5,  28, 20, 12, 4
                };  //8,16,24,32,40,48,56,64 are not used

int pc_2[48]={ 14, 17, 11, 24,  1,  5,
                3,  28, 15,  6, 21, 10,
                23, 19, 12,  4, 26,  8,
                16,  7, 27, 20, 13,  2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32 
            }; 

int p[32]={   16,  7, 20, 21, 29, 12, 28, 17,
                 1, 15, 23, 26,  5, 18, 31, 10,
                 2,  8, 24, 14, 32, 27,  3,  9,
                19, 13, 30,  6, 22, 11,  4,  25
            };

int sbox[8][64]={{ 14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
                     0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
                     4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
                    15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
                },
                {   15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
                     3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
                     0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
                    13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
                },
                {   10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
                    13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
                    13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
                     1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
                },
                {    7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
                    13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
                    10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
                     3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
                },
                {    2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
                    14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
                     4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
                    11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3,
                },
                {   12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
                    10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
                     9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
                     4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
                },
                {    4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
                    13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
                     1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
                     6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12,
                },
                {   13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
                     1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
                     7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
                     2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
                }
                };

int rotateMap[16]={0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};  //2,9,16 be 1
int* decToBinary(unsigned long long);   //translate char[] input to byte, big endian
int pow(int, int, int);  //prefix number, base, power

using namespace std;
int main(int argc, char *argv[]){
    int *key = (int*)malloc(sizeof(int)*64);
    int *cipherText = (int*)malloc(sizeof(int)*64);    //there would be maximun 48+48 bit
    //store thr transformed key
    int scheduledKey[16][56];
    int buffer[64];     //used to store temperate permutation data
    int buffer1[48];    //maximun size is 48, in f-function
    memset(buffer,0,sizeof(buffer));
    memset(buffer1,0,sizeof(buffer1));
    char *dirtyKey=argv[1];
    char *dirtyCipherText=argv[2];

    //translate input from character to binary array
    //first translate them to lower case
    strlwr(dirtyCipherText);
    strlwr(dirtyKey);

    //translate from char to decimal number.
    unsigned long long cipherTextLong = strtoull(dirtyCipherText, NULL, 16);
    unsigned long long keyLong = strtoull(dirtyKey, NULL, 16);
    //translate from long to binary array.
    cipherText = decToBinary(cipherTextLong);
    key = decToBinary(keyLong);

    //key pc-1:64 ->56, teacher said DES should readlly has 56 bit lenth key, which make a logic error here
    for(int j=0; j<=55; j++){
        buffer[j]=key[pc_1[j]-1];
    }
    //store working result
    for(int j=0; j<=55; j++){
        scheduledKey[0][j]=buffer[j];
    }
    
    //the first key need no rotation
    //generate 15 key according to the rotate rule
    for(int i=1; i<=15; i++){
        //rotate first part to right
        int x=0;
        for(int j=0; j<=27; j++){
            //shift to left, so plus
            x=j+rotateMap[i];
            if(x>27) x=x-28;  //reverse to end
            scheduledKey[i][x]=scheduledKey[i-1][j];
        }
        //rotate second part to right
        for(int j=28; j<=55; j++){
            x=j+rotateMap[i];
            if(x>55) x=x-28;  //reverse to end
            scheduledKey[i][x]=scheduledKey[i-1][j];
        }
    }
    //pc-2
    for(int i=0; i<=15; i++){
        for(int j=0; j<=47; j++){
            buffer[j]=scheduledKey[i][pc_2[j]-1];
        }
        for(int j=0; j<=47; j++){
            scheduledKey[i][j]=buffer[j];
        }
    }
    //key preprocess end

    //initial inverse permutation
    for(int i=0; i<=63; i++){
        buffer[i]=cipherText[ip[i]-1];    //maybe we can just use ip instead inverse ip
    }
    for(int i=0; i<=63; i++){
        cipherText[i]=buffer[i];
    }
    //replace right to left, left to right
    for(int i=0; i<=31; i++){
        buffer[i]=cipherText[i];
    }
    for(int i=0; i<=31; i++){
        cipherText[i]=cipherText[i+32];
    }
    for(int i=0; i<=31; i++){
        cipherText[i+32]=buffer[i];
    }
    //f-function, we don't need to reverse the f-function
    //do the following same thing for 16 times
    for(int z=0; z<=15; z++){
        //following operation are about left part
        //that where magic happened
        //expansion
        memset(buffer, 0, sizeof(buffer));
        memset(buffer1, 0, sizeof(buffer1));
        //for(int i=0; i<=63; i++) cout<<cipherText[i];
        //cout<<"\n";
        for(int i=0; i<=47; i++){
            buffer[i]=cipherText[e[i]-1];
        }
        //apply change to buffer1, which is the buffer for left part
        for(int i=0; i<=47; i++){
            buffer1[i]=buffer[i];
        }
        //xor with key
        for(int i=0; i<=47; i++){
            buffer1[i]=buffer1[i]^scheduledKey[z][i];
        }
        //sbox expansion
        //cipher text would seperate in to 8 part
        int position;
        for(int i=0; i<=7; i++){
            //get the first and last bits
            int row = pow(buffer1[i*6+0], 2, 1)+pow(buffer1[i*6+5], 2, 0);
            //get the mid four bits
            int column = pow(buffer1[i*6+1], 2, 3)+pow(buffer1[i*6+2], 2, 2)+pow(buffer1[i*6+3], 2, 1)+pow(buffer1[i*6+4], 2, 0);
            position = 16*row+column;
            //translate substitution data to binary and store as result
            int *bufferInt = decToBinary(sbox[i][position]);
            for(int j=0; j<=3; j++) buffer1[4*i+j]=bufferInt[60+j];
        }
        //permutation
        for(int i=0; i<=31; i++){
            buffer[i] = buffer1[p[i]-1];
        }
        //store the result
        for(int i=0; i<=31; i++){
            buffer1[i] = buffer[i];
        }
        //xor left with right
        for(int i=0; i<= 31; i++){
            buffer[i] = buffer1[i]^cipherText[32+i];
        }
        for(int i=0; i<= 31; i++){
            buffer1[i] = buffer[i];
        }
        //store left to right 
        for(int i=0; i<= 31; i++){
            cipherText[32+i]=cipherText[i];
        }
        //store f-function left to left
        for(int i=0; i<= 31; i++){
            cipherText[i]=buffer1[i];
        }
    }
    //reverse initial permutation
    for(int i=0; i<=63; i++){
        buffer[i] = cipherText[inverse_ip[i]-1];
    }
    for(int i=0; i<=63; i++){
        cipherText[i] = buffer[i];
    }
    //translate binary to hex array: four binary as one hex, 16 hex are there
    for(int i=0; i<=15; i++){
        cipherText[i]=  pow(cipherText[4*i+0],2,3)+pow(cipherText[4*i+1],2,2)
                       +pow(cipherText[4*i+2],2,1)+pow(cipherText[4*i+3],2,0);
        }
    //hex to character
    for(int i=0; i<=15; i++){
        if(cipherText[i] <= 9){   //0-9
            dirtyCipherText[i] = '0'+cipherText[i];
        }else{  //a-z
            dirtyCipherText[i] = 'a'+cipherText[i]-10;
        }
    }
    //output result
    cout <<"0x";
    for(int i=0; i<=15; i++){
        cout << dirtyCipherText[i];
    }
}

int* decToBinary(unsigned long long n){ 
    // array to store binary number 
    int *binaryNum;
    binaryNum= (int*)malloc(sizeof(int)*64);
    // counter for binary array 
    int i = 0;
    while (n > 0 || i<=63) {
        // storing remainder in binary array 
        binaryNum[63-i] = n % 2;
        n = n / 2;
        i++;
    }
    return binaryNum;
};

int pow(int prefix, int base, int power){  //input number:0 or 1, power base 2
    if(power == 0 )return prefix*1;

    for (int i = 0; i <=power-1; i++){
        prefix = prefix*base;
    }
    return prefix;
}; 