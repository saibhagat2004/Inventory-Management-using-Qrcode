// #include <stdio.h>

// void main() {
//     int a[100][100], i, j, n, k;

//     printf("ENTER NO. OF ROW AND COLUMN:\n");
//     scanf("%d", &n);

//     printf("ENTER MATRIX ELEMENT:\n");
//     for (i = 0; i < n; i++) {
//         for (j = 0; j < n; j++) {
//             scanf("%d", &a[i][j]);
//         }
//     }

//     for (i = 0; i < n; i++) {
//         for (j = 0; j < n; j++) {
//             if (i == j) {
//                 a[i][j] = 0;
//             }
//         }
//     }

//     printf("GIVEN MATRIX IS:\n");
//     for (i = 0; i < n; i++) {
//         for (j = 0; j < n; j++) {
//             printf(" %d ", a[i][j]);
//         }
//         printf("\n");
//     }

//     for (k = 0; k < n; k++) {
//         for (i = 0; i < n; i++) {
//             for (j = 0; j < n; j++) {
//                 if (a[i][j] > a[i][k] + a[k][j]) {
//                     a[i][j] = a[i][k] + a[k][j];
//                 } else {
//                     a[i][j] = a[i][j];
//                 }
//             }
//         }
//     }

//     printf("YOUR MATRIX IS:\n");
//     for (i = 0; i < n; i++) {
//         for (j = 0; j < n; j++) {
//             printf(" %d\t ", a[i][j]);
//         }
//         printf("\n");
//     }
// }


#include <stdio.h>
#include <string.h>

char b[10][10];
int c[10][10] ;

void lcs(char x[], char y[]) {
    int m, n;
    m = strlen(x);
    n = strlen(y);
    int i, j;

    for (i = 1; i <= m; i++) {
        c[i][0] = 0;
        b[i][0] = '-';
    }

    for (j = 1; j <= n; j++) {
        c[0][j] = 0;
        b[0][j] = '-';
    }

    for (i = 1; i <= m; i++) {
        for (j = 1; j <= n; j++) {
            if (x[i - 1] == y[j - 1]) {
                c[i][j] = c[i - 1][j - 1] + 1;
                b[i][j] = 'd'; // 'd' denotes diagonal move
            } else if (c[i - 1][j] >= c[i][j - 1]) {
                c[i][j] = c[i - 1][j];
                b[i][j] = 'u'; // 'u' denotes upward move
            } else {
                c[i][j] = c[i][j - 1];
                b[i][j] = 'l'; // 'l' denotes leftward move
            }
        }
    }
}

void printlcs(char x[], int i, int j) {
    if (i == 0 || j == 0) {
        return;
    }
    if (b[i][j] == 'd') {
        printlcs(x, i - 1, j - 1);
        printf("%c", x[i - 1]);
    } else if (b[i][j] == 'u') {
        printlcs(x, i - 1, j);
    } else {
        printlcs(x, i, j - 1);
    }
}

void main() {
    char a[100], B[100];
    printf("\nEnter first sequence:\n");
    scanf("%s", a);
    printf("\nEnter second sequence:\n");
    scanf("%s", B);
    printf("\nLongest subsequence is:\n");
    lcs(a, B);
    int x, y, i, j;
    x = strlen(a);
    y = strlen(B);
    
    printf("\nMatrix c:\n");
    for (i = 0; i <= x; i++) {
        for (j = 0; j <= y; j++) {
            printf("%3d\t", c[i][j]);
        }
        printf("\n");
    }

    printf("\nMatrix b:\n");
    for (i = 0; i <= x; i++) {
        for (j = 0; j <= y; j++) {
            printf("%3c\t", b[i][j]);
        }
        printf("\n");
    }

    printf("\nLongest common subsequence: ");
    printlcs(a, x, y);
    printf("\n\n");
}
