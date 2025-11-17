SUBDIRS = target/arch_32 target/arch_64 

.PHONY: all clean

all:
	for d in $(SUBDIRS); do \
		$(MAKE) -C $$d; \
	done

clean:
	for d in $(SUBDIRS); do \
		$(MAKE) -C $$d clean; \
	done
