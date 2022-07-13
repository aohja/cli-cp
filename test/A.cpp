/*
 * author: Aadi Ohja
 * date:   Tuesday, 12 July, 2022
 * time:   11:28:45 AM
*/
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int T;
char s[4];

int main() 
{
    scanf("%d", &T);
    while (T--) {
        scanf("%s", s);
        bool ok = true;
        if (s[0] != 'y' && s[0] != 'Y') ok = false;
        if (s[1] != 'e' && s[1] != 'E') ok = false;
        if (s[2] != 's' && s[2] != 'S') ok = false;
        if (ok) printf("YES\n");
        else printf("NO\n");
    }
    return 0;
}
