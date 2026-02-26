#ifdef _WIN32
#include "FileDialog.h"
#include <windows.h>
#include <string>

std::string openImageFile() {
	char chosenFilePath[MAX_PATH] = {};
	OPENFILENAMEA openFileName = {};
	openFileName.lStructSize = sizeof(OPENFILENAMEA);
	openFileName.lpstrFilter = "Images (*.png;*.jpg;*.jpeg;*.bmp)\0*.png;*.jpg;*.jpeg;*.bmp\0All (*.*)\0*.*\0";
	openFileName.lpstrFile = chosenFilePath;
	openFileName.nMaxFile = MAX_PATH;
	openFileName.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;
	if (GetOpenFileNameA(&openFileName) == 0) {
		return "";
	}
	return std::string(chosenFilePath);
}
#endif
