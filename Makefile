.PHONY: test

test:
		cellprofiler -c -r -p AdvancedSegmentation/BBBC022_Analysis_Final.cppipe -i AdvancedSegmentation/images -o AdvancedSegmentation/output
		rm -rf AdvancedSegmentation/output
		cellprofiler -c -r -p Translocation/Translocation_final.cppipe -i Translocation/images -o Translocation/output
		rm -rf Translocation/output
		cellprofiler -c -r -p 3d_monolayer/3d_monolayer_final.cppipe -i 3d_monolayer/images -o 3d_monolayer/output
		rm -rf 3d_monolayer/output
