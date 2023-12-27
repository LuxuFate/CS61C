#include <stddef.h>
#include "ll_cycle.h"

int ll_has_cycle(node *head) {
    node *tortoise = head;
    node *hare = head;
    while(hare){
	if(hare->next && hare->next->next){
		hare = hare->next->next;
	}else{
	    break;
	}
	tortoise = tortoise->next;
	if(hare == tortoise){
		return 1;
	}
    }
    return 0;
}
