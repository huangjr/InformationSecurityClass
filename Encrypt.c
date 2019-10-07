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
    int row;
    int column;
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
        playfair(strlwr(argv[3]), strlwr(argv[2]));
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
        rail_fence(strlwr(argv[3]), 
        argv[2]);
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
    if(strlen(plainText)%2 != 0){
        strcat(plainText, "x");
    }
    for(int i=0; i<= 25; i++){
        //add all of the character a-i k-z, skip j=9
        if(i == 9){
            //do nothing, to skip j
        }else add(i+97);
    }
    current=head;
    //traslate every j as i
    for(int i=0; i<=strlen(plainText); i++){
        if(plainText[i] == 'j'){
            plainText[i] = 'i';
        }
    }for(int i=0; i<=strlen(key)-1; i++){
        remove(key[i]);     //remove the character in plaintext, current would be in head after remove
    }
    //declare cipher map
    char cipherMap[5][5];
    int l=0;    //the anti-prevent index
    for(int i=0; i<=4; i++){
        for(int j=0; j<=4; j++){
            if((5*i+j) < strlen(key)-l){
                bool add=true;
                // to see if the adding text is in the range of removed element
                if((5*i+j) > 0){    //if init at 0 nothing would be added
                    for(int k=0; k<=(5*i+j+l-1); k++){
                        if(key[k] == key[5*i+j+l]){
                            add = false;
                            l++;                            //guide the next element to next one
                            cipherMap[i][j]=key[5*i+j+l];   //the current element haven't repeated
                        }
                    }
                }
                if(add){
                    cipherMap[i][j]=key[5*i+j+l]; //the current element haven't repeated
                }
            }else{
                current=current->next;  //because it start from head
                cipherMap[i][j] = current->character;   //segmentation fault?????
            }
        }
    }
    for(int i=0; i<= strlen(plainText)-1; i+=2){
        struct coordinate pos[3];
        for(int j=0; j<=2; j++){
            if(j <=2 ){
                pos[j]=find(plainText[i+j], cipherMap);
            }else{
                pos[j]=find('x', cipherMap);
            }
        }
        if(pos[0].column==pos[1].column && pos[0].row==pos[1].row){
            cipherText[i+0] = cipherMap[pos[2].row][pos[0].column];
            cipherText[i+1] = cipherMap[pos[0].row][pos[2].column];
        }else if(pos[0].column==pos[1].column && pos[0].row!=pos[1].row){
            cipherText[i+0] = cipherMap[((pos[0].row)+1)%5][pos[0].column];
            cipherText[i+1] = cipherMap[((pos[1].row)+1)%5][pos[0].column]; 
        }else if(pos[0].column!=pos[1].column && pos[0].row==pos[1].row){
            cipherText[i+0] = cipherMap[pos[0].row][((pos[0].column)+1)%5];
            cipherText[i+1] = cipherMap[pos[0].row][((pos[1].column)+1)%5];
        }else if(pos[0].column!=pos[1].column && pos[0].row!=pos[1].row){
            cipherText[i+0] = cipherMap[pos[0].row][pos[1].column];
            cipherText[i+1] = cipherMap[pos[1].row][pos[0].column];
        }else{
            //do nothing
        }
    }
    strupr(cipherText);
}

void vernam(char *plainText, char *key){
    //generate the Veram key
    strcat(key, plainText);
    for(int i=0; i <=strlen(plainText)-1; i++){
        cipherText[i]= (char)(((plainText[i]-97)^(key[i]-97))+95);  // 97 would exceed the limit so we set it to 95
    }
    strupr(cipherText);
}

void row(char *plainText, char *key){
    int n;  //#row of plainmap
    if(strlen(plainText)%8 == 0){
        n=strlen(plainText)/8;
    }else{
        n=strlen(plainText)/8+1;
    }
    char plainMap[n][8];
    //buildup the row access order map
    int rowMap[8];
    int columnMap[8];
    for(int i=0; i<=7; i++){
        rowMap[i]=key[i]-49;
    }
    for(int i=0; i<=7; i++){
        if(i <= (strlen(plainText)%8-1)) columnMap[i]=n;
        else columnMap[i]=n-1;
    }
    //fill the plaintext map
    for(int i=0; i<=(n-1); i++){
        for(int j=0; j<=7; j++){
            if(8*i+j <= strlen(plainText)-1){
                plainMap[i][j]=plainText[8*i+j];
            }else{
                plainMap[i][j]='0'; //no fill on empty
            }
        }
    }
    //fill the ciphertext
    int k=0;
    for(int i=0; i<=7; i++){
        for(int j=0; j<=(columnMap[rowMap[i]]-1); j++){
                cipherText[k]=plainMap[j][rowMap[i]];   //quite a bug here we jump without filling it
                k++;
        }
    }
    strupr(cipherText);
}

void rail_fence(char *plainText, char *key){
    int depth=atoi(key);
    char cipherMap[10][100];
    //empty the map
    for(int i=0; i<=9; i++){
        for(int j=0; j<=99; j++){
            cipherMap[i][j]=0;
        }
    }
    int i=0;    //index for row
    while(i <= strlen(plainText)-1){
        for(int j=0; j<(depth-1); j++){
            if(i <= strlen(plainText)-1){
                cipherMap[j][i]=plainText[i];
            }else{
                cipherMap[j][i]='0';  // in the case some shit would insert
            }
            i++;
        }
        for(int k=(depth-1); k>0; k--){
            if(i <= strlen(plainText)-1){
                cipherMap[k][i]=plainText[i];
            }else{
                cipherMap[k][i]='0';
            }
            i++;
        }
    }
    int k=0;    //index for cipherText
    for(int i=0; i<=depth-1; i++){
        for(int j=0; j<=strlen(plainText)-1; j++){
            if((cipherMap[i][j]-97) >= 0){
                cipherText[k]=cipherMap[i][j];
                k++;
            }
        }
    }
    strupr(cipherText);
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
            free(current);
            current=head;
            return 0;       // return when the wanted character found, or it would be a endless loop
        }
    }
}

coordinate find(char character, char cipherMap[5][5]){
    //linear searching take O(n), suck but it works.
    //i=j here, make them the same at first
    for(int i=0; i <= 4; i++){
        for(int j=0; j <= 4; j++){
            if(cipherMap[i][j] == character){
                return coordinate{i,j};   //i=row, j=column
            }
        }
    }
}