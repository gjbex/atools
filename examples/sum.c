#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    double sum = 0.0;
    int i;
    for (i = 1; i < argc; i++) {
        double value = atof(argv[i]);
        sum += value;
    }
    printf("%lf\n", sum);
    return 0;
}
