#! /bin/bash
# Este programa converte netlist em Qucs para netlist em Spice.
# O primeiro argumento é o input (arquivo qucs), e o segundo, o arquivo de output.
#
# Como utilizar: coloque este arquivo numa pasta qualquer (ex.: crie uma pasta
# /home/bin para colocar scripts desse tipo) e depois a adicione ao seu
# PATH com o comando: PATH=$PATH:/home/bin export PATH
#
# Depois disso, é só chamar o programa no terminal: qucs2ng file1 file2
#
# Autor: Felipe Duque

#while getopts a option
#do
#	case "${option}" in
#		a) sed -e '/.control/,/.endc/ s/a/a/'
#			<$2 >temp
#		echo ola;;
#	esac
#done

if [ "$3" = '-a' ]; then
	sed -n '/.control/,/.endc/p' <$2 >temp
fi
	

sed '{
	$a	
	s/gnd/0/g
	s/_net0/99/g
	s/_net//g

#Análise de VDC

	/Vdc:/ {
		s/"//g
		s/U=\([0-9]*\).*/\1/
		s/.\{4\}//	
	}

#Análise de R

	/R:/ {
		s/"//g
		s/R=\([0-9a-zA-Z.]*\).*/\1/
		s/.\{2\}//
	}	

#Análise de VAC

	/Vac:/ {
		s/U="\([0-9]*[a-zA-Z]*\)"/SIN(0 \1/
		s/f="\([0-9]*[a-zA-Z]*\)".*/\1)/
		s/.\{4\}//
	}	

#Análise de C

	/C:/ {
		s/C="\([0-9]*[a-zA-Z]*\).*/\1/
		s/.\{2\}//
	}

#Análise de TBJ

	/BJT:/ {
		s/.\{4\}//
		s/T\([0-9]*\)/Q\1/
		s/[a-zA-Z0-9]*[[:space:]]\(Type.*\)/\1/
		s/Type="npn.*/2n3904/
		s/Type="pnp.*/2n3906/
		s/[[:space:]]\([a-zA-Z0-9]*\)[[:space:]]\([a-zA-Z0-9]*\)/ \2 \1/	
	}

#Análise de L

	/L:/ {
		s/.\{2\}//
		s/L="\([0-9]*[a-zA-Z]*\).*/\1/
	}

#Análise de D

	/Diode:/ {
		s/[[:space:]]\([a-zA-Z0-9]*\)[[:space:]]\([a-zA-Z0-9]*\)/ \2 \1/
		s/Is.*//
		s/$/1n4009/
		s/Diode://
	}

#Análise de repetição de Vx1

	/Vx1/ {
		d
	}

#Análise de repetição de Vx2

	/Vx2/ {
		d
	}

#Análise de amp op

	/OpAmp:/ {
		s/OpAmp:OP/X/
		s/[[:space:]]\([a-zA-Z0-9]*\)[[:space:]]\([a-zA-Z0-9]*\)[[:space:]]\([a-zA-Z0-9]*\).*/ \2 \1 vccp vccm \3 lm324/
		a\Vx1 vccp 0 15
		a\Vx2 vccm 0 -15
	}

#Análise de Vpulse

	/Vpulse:/ {
		s/U1="\([0-9]*[.a-zA-Z]*\)"/PULSE(\1/
		s/U2="\([0-9]*[.a-zA-Z]*\)"/\1/
		s/T1="\([0-9]*[.a-zA-Z]*\)"/\1/
		s/T2="\(.*\)"[[:space:]]Tr="\([0-9]*[.a-zA-Z]*\)"[[:space:]]Tf="\([0-9]*[.a-zA-Z]*\)"/\2 \3 \1)/
		s/Vpulse://
	}

}' <$1 >temp2
	
if [ "$3" = '-a' ]; then
	cat temp2 temp >temp3
	rm temp
else
	mv temp2 temp3
fi

sed '{
	2a\.include /home/felipe/.spicemodels
	$a
	$a\.end
}' <temp3 >$2

