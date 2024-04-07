find_package (Python REQUIRED COMPONENTS Interpreter)

function(convert_class INPUT_PATH OUTPUT_DIR)
	set(SCRIPT_PATH "${PROJECT_SOURCE_DIR}/cmake/convert.py")
	get_filename_component(INPUT_NAME "${INPUT_PATH}" NAME_WE)


	set(${OUTPUT_DIR} "${CMAKE_BINARY_DIR}/classgen")
	set(RESULT_PATH "${${OUTPUT_DIR}}/${INPUT_NAME}.h")
	file(MAKE_DIRECTORY "${${OUTPUT_DIR}}")

	execute_process(
		COMMAND "${Python_EXECUTABLE}" "${SCRIPT_PATH}" "${INPUT_PATH}"
		OUTPUT_FILE "${RESULT_PATH}"
	)

	return(PROPAGATE ${OUTPUT_DIR})
endfunction()
