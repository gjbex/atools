CFLAGS = -O2

all: sum.exe

%.exe: %.o
	$(CC) $(CFLAGS) -o $@ $<

clean:
	$(RM) $(wildcard *.exe) $(wild_card *.o)
