#include <stdio.h>

int main(){

    char names[5][20];
    int age[5];

    for (int i = 0; i < 5; i++) {
        printf("Enter Name: ");
        scanf("%s", names[i]);

        printf("Enter Age: ");
        scanf("%d", &age[i]);
    }

    for (int i = 0; i < 5; i++) {  // Loop should go from 0 to 4
        printf("Name: %s  Age: %d\n", names[i], age[i]);
    }

    return 0;
}
