#include <string.h>
#include <stdio.h>

// d like DIR
#define Ud 0x10
#define Rd 0x20
#define Dd 0x30
#define Ld 0x40

// b like BITMASK
#define Ub 0b0001
#define Rb 0b0010
#define Db 0b0100
#define Lb 0b1000

/*
gcc -O2 -fPIC -shared -ldl -o libday6.so day6.c
*/

int c_bitmask_solve(const int istart, const int jstart,
                    __uint8_t *matrix, int m, int n)
{
    char work_matrix[m][n];
    memset(work_matrix, 0, m * n * sizeof(char));

    work_matrix[istart][jstart] = Ud | Ub;

    int ii = istart;
    int jj = jstart;

    char c, cl, dl;
    while(ii >= 0 && jj >= 0 && ii < m && jj < n)
    {
        c = work_matrix[ii][jj];
        cl = c & 0xf0;
        dl = c & 0x0f;

        //printf("%d [%d][%d] %d\n", c, ii, jj, matrix[ii * n + jj]);

        switch (cl) {
            case Ud:
                if (ii > 0 && matrix[(ii-1) * n + jj] == 1) {
                    if (c & Rb) return -1;
                    work_matrix[ii][jj] = Rd | Rb | dl;
                } else {
                    work_matrix[ii][jj] = dl | Ub;
                    if (ii > 0)
                        //work_matrix[ii-1][jj] |= Ud | Ub;
                        work_matrix[ii-1][jj] = Ud | Ub | (work_matrix[ii-1][jj] & 0x0f);
                    --ii;
                }
                break;
            case Rd:
                if (jj < n-1 && matrix[ii * n + jj+1] == 1) {
                    if (c & Db) return -1;
                    work_matrix[ii][jj] = Dd | Db | dl;
                } else {
                    work_matrix[ii][jj] = dl | Rb;
                    if (jj < n-1)
                        //work_matrix[ii][jj+1] |= Rd | Rb;
                        work_matrix[ii][jj+1] = Rd | Rb | (work_matrix[ii][jj+1] & 0x0f);
                    ++jj;
                }
                break;
            case Dd:
                if (ii < m-1 && matrix[(ii+1) * n + jj] == 1) {
                    if (c & Lb) return -1;
                    work_matrix[ii][jj] = Ld | Lb | dl;
                } else {
                    work_matrix[ii][jj] = dl | Db;
                    if (ii < m-1)
                        //work_matrix[ii+1][jj] |= Dd | Db;
                        work_matrix[ii+1][jj] = Dd | Db | (work_matrix[ii+1][jj] & 0x0f);
                    ++ii;
                }
                break;
            case Ld:
                if (jj > 0 && matrix[ii * n + jj - 1] == 1) {
                    if (c & Ub) return -1;
                    work_matrix[ii][jj] = Ud | Ub | dl;
                } else {
                    work_matrix[ii][jj] = dl | Lb;
                    if (jj > 0)
                        //work_matrix[ii][jj-1] |= Ld | Lb;
                        work_matrix[ii][jj-1] = Ld | Lb | (work_matrix[ii][jj-1] & 0x0f);
                    --jj;
                }
                break;
        }
    }

    int cnt = 0;
    //printf("Returning ---------\n");
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            if (work_matrix[i][j] > 0)
                ++cnt;
    
    //printf("Returning %d\n", cnt);
    return cnt;
}