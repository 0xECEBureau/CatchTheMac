#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>

#define ROCK 0
#define PAPER 1
#define SCISSORS 2

#define CLEAR printf("\033[H\033[J");

void print_ascii_art()
{
    printf("\n");
    printf("$$\\      $$\\                     $$$$$$$\\                                         $$$$$$\\            $$\\\n");
    printf("$$$\\    $$$ |                    $$  __$$\\                                       $$  __$$\\           \\__|\n");
    printf("$$$$\\  $$$$ | $$$$$$\\   $$$$$$$\\ $$ |  $$ |$$$$$$\\   $$$$$$\\   $$$$$$\\   $$$$$$\\ $$ /  \\__| $$$$$$$\\ $$\\  $$$$$$$\\  $$$$$$$\\  $$$$$$\\   $$$$$$\\   $$$$$$$\\\n");
    printf("$$\\$$\\$$ $$ | \\____$$\\ $$  _____|$$$$$$$  |\\____$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\\\$$$$$$\\  $$  _____|$$ |$$  _____|$$  _____|$$  __$$\\ $$  __$$\\ $$  _____|\n");
    printf("$$ \\$$$  $$ | $$$$$$$ |$$ /      $$  ____/ $$$$$$$ |$$ /  $$ |$$$$$$$$ |$$ |  \\__|\\____$$\\ $$ /      $$ |\\$$$$$$\\  \\$$$$$$\\  $$ /  $$ |$$ |  \\__|\\$$$$$$\\\n");
    printf("$$ |\\$  /$$ |$$  __$$ |$$ |      $$ |     $$  __$$ |$$ |  $$ |$$   ____|$$ |     $$\\   $$ |$$ |      $$ | \\____$$\\  \\____$$\\ $$ |  $$ |$$ |       \\____$$\\\n");
    printf("$$ | \\_/ $$ |\\$$$$$$$ |\\$$$$$$$\\ $$ |     \\$$$$$$$ |$$$$$$$  |\\$$$$$$$\\ $$ |     \\$$$$$$  |\\$$$$$$$\\ $$ |$$$$$$$  |$$$$$$$  |\\$$$$$$  |$$ |      $$$$$$$  |\n");
    printf("\\__|     \\__| \\_______| \\_______|\\__|      \\_______|$$  ____/  \\_______|\\__|      \\______/  \\_______|\\__|\\_______/ \\_______/  \\______/ \\__|      \\_______/\n");
    printf("                                                    $$ |\n");
    printf("                                                    $$ |\n");
    printf("                                                    \\__|\n");
    printf("\n");
}

void get_input(unsigned int * input){
    printf("Enter 0 (rock), 1 (paper), 2 (scissors) :\nPS : use Ctrl - C to quit ;)\n");
    scanf("%d",input);
    if (*input > 2 | *input < 0){
        printf("\nBAD INPUT : EXITING\n");
        fflush(stdout);
        exit(0);
    }
}

// Rock paper scissors from : https://gist.github.com/wynand1004/b5c521ea8392e9c6bfe101b025c39abe
void print_rock(){
    printf("\n");
    printf("    _______\n");
    printf("---'   ____)\n");
    printf("      (_____)\n");
    printf("      (_____)\n");
    printf("      (____)\n");
    printf("---.__(___)\n");
    printf("\n");
}
void print_paper(){
    printf("\n");
    printf("     _______\n");
    printf("---'    ____)____\n");
    printf("           ______)\n");
    printf("          _______)\n");
    printf("         _______)\n");
    printf("---.__________)\n");
    printf("\n");
}
void print_scissors(){
    printf("\n");
    printf("    _______\n");
    printf("---'   ____)____\n");
    printf("          ______)\n");
    printf("       __________)\n");
    printf("      (____)\n");
    printf("---.__(___)\n");
    printf("\n");
}

void print_rock_paper_scissors(int which){
    switch (which) {
    case ROCK:
        print_rock();
    break;
    case PAPER:
        print_paper();
    break;
    case SCISSORS:
        print_scissors();
    break;
    default:
        printf("\nerror\n");
        exit(0);
        break;
    }
}

// l1ck_h15_t03_t0_93t_fl49
uint32_t flag_key;
char flag[25] = {0x17,0x59,0x49,0x7d,0x24,0x00,0x1b,0x23,0x24,0x1c,0x1a,0x25,0x24,0x1c,0x1a,0x49,0x42,0x5b,0x5e,0x49,0x1d,0x04,0x1e,0x2f,0};
void print_flag(){
    char flag_decrypt[25] = {0};
    uint32_t*flag_decrypt_ = (uint32_t*)flag_decrypt;
    uint32_t*flag_ = (uint32_t*)flag;
    for (int i=0;i<6;i++){
        flag_decrypt_[i] = flag[i] ^ flag_key;
    }
    printf("\nflag : MAC{%s}\n",flag_decrypt);
    fflush(stdout);
    exit(0);
}

int main(){
    unsigned int nb_win=0;
    unsigned int bot_response;
    unsigned int player_response;
    flag_key = 0;

    srand(0xDEADBEEF);
    CLEAR
    print_ascii_art();
    while(1){
        get_input(&player_response);
        bot_response = rand()%3;
        CLEAR
        print_ascii_art();
        printf("\nYou :\n");
        print_rock_paper_scissors(player_response);
        printf("\nBot :\n");
        print_rock_paper_scissors(bot_response);
        if (bot_response == player_response){
            printf("\nIt's a tie !!\n");
            nb_win = 0;
        }
        else if(bot_response == ROCK){
            if (player_response == PAPER){
                printf("\nYou win !!\n");
                nb_win++;
            }
            else{
                printf("\nYou lose !!\n");
               nb_win = 0;
            }
        }
        else if(bot_response == PAPER){
            if (player_response == SCISSORS){
                printf("\nYou win !!\n");
                nb_win++;
            }
            else{
                printf("\nYou lose !!\n");
                nb_win = 0;
            }
        }
        else{
            if (player_response == ROCK){
                printf("\nYou win !!\n");
                nb_win++;
            }
            else{
                printf("\nYou lose !!\n");
                nb_win = 0;
            }
        }
        if(nb_win)
            flag_key = ((flag_key << 1)|(flag_key >> 31)) + player_response;
        else
            flag_key = 0;
        if(nb_win == 1000){
            print_flag();
        }
    }
    return 0;
}
