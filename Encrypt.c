#include <cstdlib>
#include <stdlib.h>
#include <iostream>
#include <string.h>

//cipher declaration
void caesar(char *plainText, int key);

void playfair(char *plainText, char *key);

void vernam(char *plainText, char *key);

void row(char *plainText, char *key);

void rail_fence(char *plainText, char *key);

char cipherText[100];
using namespace std;
int main(int argc, char *argv[]){  // form = {cipher} {key} {plaintext}
    if(strcmp(argv[1], "caesar") == 0){
        caesar(argv[3], atoi(argv[2]));
        for(int i =0; i <= strlen(argv[3])-1; i++){
            cout << cipherText[i];
        }
    }else if(strcmp(argv[1], "playfair") == 0){
        playfair(argv[3], argv[2]);
    }else if(strcmp(argv[1], "vernam") == 0){
        vernam(argv[3], argv[2]);
    }else if(strcmp(argv[1], "row") == 0){
        row(argv[3], argv[2]);
    }else if(strcmp(argv[1], "rail_fence")== 0){
        rail_fence(argv[3], argv[2]);
    }else{
        //do nothing
    }
}

void caesar(char *plainText, int key){
    for(int i=0; i <= strlen(plainText)-1; i++){
        cipherText[i]=(plainText[i]-32+key)%91;
    }
}

void playfair(char *plainText, char *key){

}

void vernam(char *plainText, char *key){

}

void row(char *plainText, char *key){

}

void rail_fence(char *plainText, char *key){

}