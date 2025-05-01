// pprogram used to generate the encryption for MacPaperScissors
#include<stdlib.h> 
#include<stdio.h> 
//#include<string.h>
//#include <openssl/sha.h>
#include<stdint.h>

#define NB_GAMES 2

char games[NB_GAMES][50] = 
{
    "MacNumberGuess",
    "MacPaperScissors"
};

char games_pass[NB_GAMES][50] =
{
    "_n0t_m4c&ch3353_",
    "l1ck_h15_t03_t0_93t_fl49"
};
/*
char games_pass_hash[NB_GAMES][SHA256_DIGEST_LENGTH] =
{
    {0xbd,0xe6,0xc6,0x8e,0x35,0x52,0x01,0x14,0xb4,0x9f,0x0d,0xab,0x75,0xa6,0x34,0x1f,0xb2,0x38,0x0e,0x7e,0x92,0x42,0x64,0x80,0x65,0x3d,0xe1,0x3d,0xa7,0x6b,0xcd,0x32},
    {0x6e,0xb7,0xb1,0x3b,0xb7,0xd4,0x7a,0xfc,0x96,0xdd,0x62,0x48,0x1a,0xd9,0x16,0xe6,0xe7,0x9d,0x03,0x0f,0x7f,0x21,0x03,0x8c,0xbc,0x93,0x80,0xf6,0x26,0xc1,0x83,0x0b}
};
*/
char game_pass_xor_32b[NB_GAMES][50]=
{
    {},
    {}
};

/*
void hash_sha256(const char *str, unsigned char *output) {
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, str, strlen(str));
    SHA256_Final(output, &sha256);
}
*/

#define ROCK 0
#define PAPER 1 
#define SCISSORS 2

int main(){
    // shasum
    /*for(int i = 0; i<NB_GAMES; i++){
        unsigned char hash[SHA256_DIGEST_LENGTH];
        hash_sha256(games_pass[i], hash);
        printf("%s : ",games[i]);
        for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
            printf("%02x", hash[i]);
        printf("\n");
        printf((strncmp(games_pass_hash[i],hash,SHA256_DIGEST_LENGTH) == 0)?"true":"false");
        printf("\n");
    }*/

    // xor
    uint32_t gen_key = 0;
    int res =0;
    srand(0xDEADBEEF);
    for(int i=0; i<1000;i++){
        res = rand()%3;
        switch (res) {
            case ROCK:
                res = PAPER;
                break;
            case PAPER:
                res= SCISSORS;
                break;
            case SCISSORS:
                res = ROCK;
                break;
            default:
                printf("erreur");
                break;
        }
        gen_key = ((gen_key << 1)|(gen_key >> 31)) + res; 
    }
    uint32_t games_pass_crypt[6];
    uint32_t * games_pass_ = (uint32_t*)games_pass; 
    for (int i=0;i<6;i++){
        games_pass_crypt[i] = games_pass_[i] ^ gen_key;
    }
    char*games_pass_crypt_ = (char*)games_pass_crypt;
    for (int i = 0; i < 24; i++)
    {printf("%02x ", games_pass_crypt_[i]);
    }
    char games_pass_decrypt[25] = {0};
    uint32_t*games_pass_decrypt_ = (uint32_t*)games_pass_decrypt;
    for (int i=0;i<6;i++){
        games_pass_decrypt_[i] = games_pass_crypt[i] ^ gen_key;
    }
    printf("\npassword : %s\nkey : %x",games_pass_decrypt,gen_key);
    
    return 0;
}