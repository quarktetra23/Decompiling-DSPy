#include "out.h"



int entry(void)

{
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = 0;
  for (local_c = 0; local_c < 5; local_c = local_c + 1) {
    local_8 = local_8 + local_c;
  }
  return local_8;
}



