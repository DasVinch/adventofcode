#include <map>
#include <unordered_map>
#include <iostream>
#include <cassert>

#include <chrono>
using namespace std::chrono;

// g++ -O3 -o day11.exe day11.cpp

const long example[] = {125, 17};
const long input[] = {8069, 87014, 98, 809367, 525, 0, 9494914, 5};

// Only for pairs of std::hash-able types for simplicity.
// You can of course template this struct to allow other hash functions
struct pair_hash {
    template <class T1, class T2>
    std::size_t operator () (const std::pair<T1,T2> &p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);

        // Mainly for demonstration purposes, i.e. works but is overly simple
        // In the real world, use sth. like boost.hash_combine
        return h1 ^ h2;  
    }
};

using PLL = std::pair<long, long>;
using Unordered_map = std::unordered_map<PLL, long, pair_hash>;

PLL upper_pow10(long v, int k) {
    long vv = v;
    for (int kk = 0; kk < k; ++kk) {
        vv /= 10;
    }
    long ww = vv;
    for (int kk = 0; kk < k; ++kk) {
        ww *= 10;
    }
    return std::pair<long, long>(vv, v - ww);
}

int countdigits(long v)
{
    if(v < 10)
    {
        return 1;
    }
    return countdigits(v / 10) + 1;
}

long blink_but_count(long value, long n)
{
    static Unordered_map mem;
    long res = 0;

    if (n == 0) {
        return 1;
    }

    std::pair<long, long> p(value, n);

    if(mem.find(p) != mem.end())
    {
        return mem[p];
    }

    if (value == 0) {
        res = blink_but_count(1, n-1);
        mem[p] = res;
        return res;
    }

    int k = countdigits(value);
    if (k % 2 == 0) {
        auto pp = upper_pow10(value, k / 2);
        res = blink_but_count(pp.first, n-1) + blink_but_count(pp.second, n-1);
        mem[p] = res;
        return res;
    }

    res = blink_but_count(value * 2024, n-1);
    mem[p] = res;
    return res;
}

int main()
{
    long total = 0;
    for (long k: example) {
        total += blink_but_count(k, 25);
    }
    std::cout << "test p1:  " << total << std::endl;

    total = 0;
    for (long k: input) {
        total += blink_but_count(k, 25);
    }
    std::cout << "real p1:  " << total << std::endl;

    total = 0;
    for (long k: example) {
        total += blink_but_count(k, 75);
    }
    std::cout << "test p2:  " << total << std::endl;

    auto start = high_resolution_clock::now();
    total = 0;
    for (long k: input) {
        total += blink_but_count(k, 75);
    }
    std::cout << "real p2:  " << total << std::endl;
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(stop - start);

    std::cout << "Time real input p2:  " << duration.count() << " microsecs" << std::endl;

    return 0;
}