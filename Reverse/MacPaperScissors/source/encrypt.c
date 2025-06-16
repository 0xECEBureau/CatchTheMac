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

char game_pass_xor_32b[NB_GAMES][50]=
    {
        {},
        {}
    };


#define ROCK 0
#define PAPER 1
#define SCISSORS 2

int main(){

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
    uint32_t * games_pass_ = (uint32_t*)games_pass[1];
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
