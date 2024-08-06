//************************Samson Kinyanjui*********************/
#include <stdio.h>

int main()
{
    int age;
    char name[50];  // Use an array to store a string (name) instead of a single character
    float height;

    printf("Hello, Welcome to C Programming 101\n");

    printf("Please enter your name:\n");
    fgets(name, sizeof(name), stdin);  // Use fgets to read the entire line including spaces

    printf("Please enter your age:\n");
    scanf("%d", &age);

    printf("Please enter your height:\n");
    scanf("%f", &height);

    // Note: The following printf statements should include the variables in the format string
    printf("Your Name is: %s\n", name);  // %s is used to print strings
    printf("Your Age is: %d\n", age);    // %d is used to print integers
    printf("Your Height is: %.2f\n", height);  // %.2f is used to print floating-point numbers with 2 decimal places

    return 0;
}
