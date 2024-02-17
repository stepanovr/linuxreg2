#include <stdio.h>
//#include <sys/io.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdint.h>




char* mem_access(void* p_addr, uint64_t value, int bits, int read);


//To check execute in bash: "getconf PAGESIZE"
#define MAP_PAGESIZE 4096UL

#define RESULT_LEN 30
char result[RESULT_LEN];

void read8(void* v_addr, char* result)
{
  snprintf(result, RESULT_LEN, "%02X", *((volatile uint8_t*)v_addr));
}

void read16(void* v_addr, char* result)
{
  snprintf(result, RESULT_LEN, "%04X", *((volatile uint16_t*)v_addr));
}

void read32(void* v_addr, char* result)
{
  snprintf(result, RESULT_LEN, "%08lX", *((volatile uint32_t*)v_addr));
}

void read64(void* v_addr, char* result)
{
//  uint64_t read_result = *((volatile uint64_t *)v_addr);
  snprintf(result, RESULT_LEN, "%08lX%08lX", *((volatile uint32_t*)(v_addr+4)), *((volatile uint32_t*)v_addr));
}

void write8(void* v_addr, uint8_t value)
{
  *((volatile uint8_t*)v_addr) = value;
}

void write16(void* v_addr, uint16_t value)
{
  *((volatile uint16_t*)v_addr) = value;
}

void write32(void* v_addr, uint64_t value)
{
  *((volatile uint32_t*)v_addr) = value;
}

void write64(void* v_addr, uint64_t value)
{
//  *((volatile uint64_t*)v_addr) = value;
}

char* mem_access(void* p_addr, uint64_t value, int bits, int read)
{
  uint64_t page, offset;
  void* pMem;
  void* v_addr;
  int fd;

  page = ((uint64_t)p_addr / MAP_PAGESIZE) * MAP_PAGESIZE;
  offset = (uint64_t)p_addr % MAP_PAGESIZE;


  if((fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0)\
  {
    printf("failed to open /dev/mem\n");
    exit(-1);
  }

  pMem = mmap(NULL,MAP_PAGESIZE,(PROT_READ | PROT_WRITE),MAP_SHARED,
              fd,page);

  if((pMem == MAP_FAILED) || (pMem == NULL))
  {
    perror("failed to map /dev/mem");
    exit(-1);
  }

  v_addr = pMem + offset;

  if(!read)
  {
    result[0] = ' ';
    result[1] = '\0';

    //Write
    switch(bits)
    {
      case 8:
        write8(v_addr, (uint8_t)value);
        break;

      case 16:
        write16(v_addr, (uint16_t)value);
        break;

      case 32:
        write32(v_addr, (uint64_t)value);
        break;

      case 64:
        write32(v_addr, (uint64_t)value);
        write32(v_addr+4, (uint64_t)(value>>32));
        break;

      default:
        printf("Wrong bitsize\n");
    }
  }
  else
  {
    switch(bits)
    {
      case 8:
        read8(v_addr, result);
        break;

      case 16:
        read16(v_addr, result);
        break;

      case 32:
        read32(v_addr, result);
        break;

      case 64:
        read64(v_addr, result);
        break;

      default:
        printf("Wrong bitsize\n");

    }
  }
  munmap(pMem, MAP_PAGESIZE);
  close(fd);

  return result;
}

