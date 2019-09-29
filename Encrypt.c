#include <cstdlib>
#include <stdlib.h>
#include <iostream>
#include <string.h>

//character list structure
typedef struct charList{
    char character;
    struct charList *next;    
}charList;
//coordiante of playfair
typedef struct coordinate
{
    int column;
    int row;
}coordinate;
//method for searching coordinate of plaintext in playfair
coordinate find(char character, char cipherMap[5][5]);

//cipher declaration
void caesar(char *plainText, int key);
void playfair(char *plainText, char *key);
void vernam(char *plainText, char *key);
void row(char *plainText, char *key);
void rail_fence(char *plainText, char *key);

//method for charList
void add(char character);
int remove(char character);
// void search(char character);
//member for charList operation
charList *head;
charList *current;


char cipherText[100];
using namespace std;
int main(int argc, char *argv[]){  // form = {cipher} {key} {plaintext}
    if(strcmp(argv[1], "caesar") == 0){
        caesar(strlwr(argv[3]), atoi(argv[2]));
        for(int i =0; i <= strlen(argv[3])-1; i++){
            cout << cipherText[i];
        }
    }else if(strcmp(argv[1], "playfair") == 0){
        playfair(strlwr(argv[3]), argv[2]);
        for(int i =0; i <= strlen(argv[3])-1; i++){
            cout << cipherText[i];
        }
    }else if(strcmp(argv[1], "vernam") == 0){
        vernam(strlwr(argv[3]), argv[2]);
        for(int i =0; i <= strlen(argv[3])-1; i++){
            cout << cipherText[i];
        }
    }else if(strcmp(argv[1], "row") == 0){
        row(strlwr(argv[3]), argv[2]);
        for(int i =0; i <= strlen(argv[3])-1; i++){
            cout << cipherText[i];
        }
    }else if(strcmp(argv[1], "rail_fence")== 0){
        rail_fence(strlwr(argv[3]), argv[2]);
        for(int i =0; i <= strlen(argv[3])-1; i++){
            cout << cipherText[i];
        }
    }else{
        //do nothing
    }
}

void caesar(char *plainText, int key){
    for(int i=0; i <= strlen(plainText)-1; i++){
        if((plainText[i]-32+key)%91 <= 65){
            cipherText[i]=(plainText[i]-32+key)%91+65;
        }else{
            cipherText[i]=(plainText[i]-32+key);
        }
   }
}

void playfair(char *plainText, char *key){
    //build up the charList with a-z
    head=(charList*)malloc(sizeof(charList));   //empty head
    head->next=NULL;
    current=head;
    for(int i=0; i<= 25; i++){
        //add all of the character a-z
        if(i == 9){
            //do nothing
        }else add(i+97);
    }
    current=head;
    //traslate every j as i
    for(int i=0; i<=strlen(plainText); i++){
        if(plainText[i] == 'j'){
            plainText[i] = 'i';
        }
    }
    //declare cipher map
    char cipherMap[5][5];
    for(int i=0; i<=4; i++){
        for(int j=0; j<=4; j++){
            if((5*i+j) < strlen(key)-1){
                cipherMap[i][j]=key[5*i+j];
                remove(key[5*i+j]);
            }else{
                current=current->next;
                cipherMap[i][j]= current->character;
            }
        }
    }
    for(int i=0; i<= strlen(plainText)-1; i+=2){
        struct coordinate pos[2];
        for(int j=0; j<=1; j++){
            pos[j]=find(plainText[i+j], cipherMap);
        }
        if(pos[0].column==pos[1].column && pos[0].row==pos[1].row){
            pos[1].column=3;    //any random number
            pos[1].column=4;
            cipherText[i+0] = cipherMap[pos[0].row][pos[1].column];
            cipherText[i+1] = cipherMap[pos[1].row][pos[0].column];
        }else if(pos[0].column==pos[1].column && pos[0].row!=pos[1].row){
            cipherText[i+0] = cipherMap[pos[0].column][((pos[0].row)+1)%5];
            cipherText[i+1] = cipherMap[pos[0].column][((pos[1].row)+1)%5]; 
        }else if(pos[0].column!=pos[1].column && pos[0].row==pos[1].row){
            cipherText[i+0] = cipherMap[((pos[0].column)+1)%5][pos[0].row];
            cipherText[i+1] = cipherMap[((pos[1].column)+1)%5][pos[0].row];
        }else if(pos[0].column!=pos[1].column && pos[0].row!=pos[1].row){
            cipherText[i+0] = cipherMap[pos[1].row][pos[0].column];
            cipherText[i+1] = cipherMap[pos[0].row][pos[1].column];
        }else{
            //do nothing
        }
    }
}

void vernam(char *plainText, char *key){
    //generate the Veram key
    strcat(key, plainText);
    for(int i=0; i <=strlen(plainText)-1; i++){
        cipherText[i]= ((plainText[i]-97)^(key[i]-97))+97;
    }
}

void row(char *plainText, char *key){
    int n=strlen(plainText)/8;
    char plainMap[n][8];
    //buildup the row access order map
    int rowMap[8];
    for(int i=0; i<=7; i++){
        rowMap[i]=key[i]-49;
    }
    //fill the plaintext map
    for(int i=0; i<=(n-1); i++){
        for(int j=0; j<=7; j++){
            if(8*i+j <= strlen(plainText)){
                plainMap[i][j]=plainText[8*i+j];
            }else{
                plainMap[i][j]='0'; //no fill on empty
            }
        }
    }
    //fill the ciphertext map
    for(int i=0; i<=7; i++){
        for(int j=0; j<=(n-1); j++){
            if(plainMap[j][rowMap[i]] != '0'){
                cipherText[4*i+j]=plainMap[j][rowMap[i]];
            }
        }
    }
}

void rail_fence(char *plainText, char *key){
    int depth=key[0]-48;       //the depth of rail fence
    int distance[depth];    //the distance between adjacent number
    for(int i=0; i<=depth-1; i++){
        if(i == depth-1) distance[i]=distance[0];  //the distance of the last level is the same as the first
        else distance[i]=(depth-1-i)*2;
    }
    int k=0;    //index for output
    for(int i=0; i<=depth-1; i++){
        int j=0;
        while(distance[i]*j+i <= strlen(plainText)-1){
            cipherText[k]=plainText[distance[i]*j+i];
            j++;
            k++;
        }
    }
}

void add(char character){
    //add to the tail of linked list
    while(current->next != NULL){
        current=current->next;
    }
    charList *newList;
    newList= new charList;
    newList->character=character;
    newList->next=NULL;
    current->next=newList;
}

int remove(char character){
    charList *pre;
    current=head;
    //search the wanted char
    while(current->next != NULL){
        pre=current;
        current=current->next;
        if(current->character == character){
            pre->next=current->next;
            delete current;
            current=head;
            return 0;
        }
    }
}

coordinate find(char character, char cipherMap[5][5]){
    //linear searching take O(n), suck but it works.
    //i=j here, make them the same at first
    int a,b;
    for(int i=0; i <= 4; i++){
        for(int j=0; j <= 4; j++){
            if(cipherMap[i][j] == character){
                a=i;
                b=j;
            }
        }
    }
    return coordinate{b,a};   //j=column, i=row
}