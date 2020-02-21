OUTS=out/a_example.out out/b_read_on.out out/c_incunabula.out out/d_tough_choices.out out/e_so_many_books.out out/f_libraries_of_the_world.out
DATAS=a_example.data b_read_on.data c_incunabula.data d_tough_choices.data e_so_many_books.data f_libraries_of_the_world.data

all: $(OUTS)
datas: $(DATAS)
a: out/a_example.out
b: out/b_read_on.out
c: out/c_incunabula.out
d: out/d_tough_choices.out
e: out/e_so_many_books.out
f: out/f_libraries_of_the_world.out

%.data: %.txt
	@echo START $@
	@python3 setup.py $@ < $<
	@echo DONE $@

out/%.out: %.data
	@echo START $@
	@python3 hashcode.py $< $@
	@echo DONE $@

#.PHONY: all datas $(OUTS)
