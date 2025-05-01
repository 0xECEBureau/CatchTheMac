#include <stddef.h>
#include<stdio.h> 
#include<stdlib.h> 
#include<sys/mman.h>
#include<fcntl.h>
#include<unistd.h>
#include<string.h>
#include <openssl/sha.h>


#define CLEAR printf("\033[H\033[J");

#define NB_GAMES 3
#define SZ_PASSWD 50

char games[NB_GAMES][50] = 
{
    "MacNumberGuess",
    "MacPaperScissors",
    "MYams"
};

void print_ascii_art()
{
    CLEAR
    printf("\n");
    printf("$$\\      $$\\                      $$$\\      $$$$$$\\\n");                                    
    printf("$$$\\    $$$ |                    $$ $$\\    $$  __$$\\\n");
    printf("$$$$\\  $$$$ | $$$$$$\\   $$$$$$$\\ \\$$$\\ |   $$ /  \\__| $$$$$$\\  $$$$$$\\$$$$\\   $$$$$$\\\n");
    printf("$$\\$$\\$$ $$ | \\____$$\\ $$  _____|$$\\$$\\$$\\ $$ |$$$$\\  \\____$$\\ $$  _$$  _$$\\ $$  __$$\\\n"); 
    printf("$$ \\$$$  $$ | $$$$$$$ |$$ /      $$ \\$$ __|$$ |\\_$$ | $$$$$$$ |$$ / $$ / $$ |$$$$$$$$ |\n");
    printf("$$ |\\$  /$$ |$$  __$$ |$$ |      $$ |\\$$\\  $$ |  $$ |$$  __$$ |$$ | $$ | $$ |$$   ____|\n");
    printf("$$ | \\_/ $$ |\\$$$$$$$ |\\$$$$$$$\\  $$$$ $$\\ \\$$$$$$  |\\$$$$$$$ |$$ | $$ | $$ |\\$$$$$$$\\\n"); 
    printf("\\__|     \\__| \\_______| \\_______| \\____\\__| \\______/  \\_______|\\__| \\__| \\__| \\_______|\n");
    printf("\n");
}

void print_greetings()
{
    print_ascii_art();
    printf("Welcome to Mac&Game !\n");
    printf("The famous (or not) game launcher by Mac !\n");
    printf("\n");
}
// c_l_h3ure_du_du3l
char flag[18]={0x83,0xbf,0x8c,0xbf,0x88,0xd3,0x95,0x92,0x85,0xbf,0x84,0x95,0xbf,0x84,0x95,0xd3,0x8c,0x00};
void authenticate()
{
    char password[SZ_PASSWD];
    printf("Enter your password to enable Mac&Game :\n");
    scanf("%49s",password);
    int size = strlen(password);
    for(int i =0;i<size;i++)
        password[i] ^= 0xe0;
    if (strncmp(password,flag,SZ_PASSWD) != 0) 
    {
        printf("You shall not pass !\n");
        exit(0);
    }
}

void load_number_guess(){
    FILE* fd_orig = fopen("MacNumberGuess", "r");
    if (fd_orig == 0 ){
        printf("ERROR CAN NOT OPEN FILE");
        exit(0);
    }

    void *shellcode = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
        MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (shellcode == MAP_FAILED) {
        printf("ERROR CAN NOT MAP");
        exit(0);
    }

    fread(shellcode, 1, 2048, fd_orig);

    void (*func)(void) = shellcode;
    func();
}

void load_rock_paper_scissors(){
    char buffer[50*1024];
    FILE* fd_orig = fopen("MacPaperScissors", "r");
    FILE* fd_copy = fopen("/tmp/proc", "wb");
    if (fd_orig == 0 | fd_copy == 0){
        printf("ERROR CAN NOT OPEN FILES");
        exit(0);
    }
    unsigned long size = fread(buffer,1,50*1024,fd_orig);
    buffer[1] = 'E';
    buffer[2] = 'L';
    buffer[3] = 'F';

    fwrite(buffer,1,size,fd_copy);

    fclose(fd_orig);
    fclose(fd_copy);

    system("chmod +x /tmp/proc");
    system("/tmp/proc");

    system("rm /tmp/proc");
}

void load_myams(){
    system("python MYams");
}

void load_game()
{
    print_ascii_art();
    printf("You are connected !\n");
    printf("You can now choose a Game :\n");
    for(int i  = 0;i < NB_GAMES;i++)
    {
        printf("\t%d\t%s\n",i+1,games[i]);
    }
    printf("PS : use Ctrl - C to quit ;)\n");
    int input = -1;
    scanf("%d",&input);
    switch (input) {
        case 1:
            load_number_guess();
            break;
        case 2:
            load_rock_paper_scissors();
            break;
        case 3:
            load_myams();
        break;
        default:
            printf("\n BAD INPUT : EXITING\n");
            fflush(stdout);
            exit(0);
            break;
    }
    
}



int main(void)
{
    print_greetings();
    authenticate();
    load_game();
    return 0;
}