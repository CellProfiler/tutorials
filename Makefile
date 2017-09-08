.PHONY: clean test

clean:
		rm -rf 3d_monolayer/output
		rm -rf AdvancedSegmentation/output
		rm -rf Translocation/output

test:
		cellprofiler -c -r -p 3d_monolayer/3d_monolayer_final.cppipe \
		    -i 3d_monolayer/images                                   \
		    -o 3d_monolayer/output                                   \
		    -d 3d_monolayer/output/done

		cellprofiler -c -r -p AdvancedSegmentation/BBBC022_Analysis_Final.cppipe \
		    -i AdvancedSegmentation/images                                       \
		    -o AdvancedSegmentation/output                                       \
		    -d AdvancedSegmentation/output/done

		cellprofiler -c -r -p Translocation/Translocation_final.cppipe \
		    -i Translocation/images                                    \
		    -o Translocation/output                                    \
		    -d Translocation/output/done

		@if [ $$(cat 3d_monolayer/output/done) = Failure ] ||         \
		    [ $$(cat AdvancedSegmentation/output/done) = Failure ] || \
		    [ $$(cat Translocation/output/done) = Failure ]; then     \
		    false;                                                    \
		else true; fi