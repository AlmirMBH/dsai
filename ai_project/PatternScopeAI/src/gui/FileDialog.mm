#import <Cocoa/Cocoa.h>
#include "FileDialog.h"

std::string openImageFile() {
    NSOpenPanel* panel = [NSOpenPanel openPanel];
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdeprecated-declarations"
    [panel setAllowedFileTypes:@[@"png", @"jpg", @"jpeg", @"bmp", @"tga"]];
#pragma clang diagnostic pop
    [panel setAllowsOtherFileTypes:NO];
    if ([panel runModal] != NSModalResponseOK) {
        return "";
    }
    NSURL* url = [[panel URLs] objectAtIndex:0];
    const char* path = [[url path] UTF8String];
    return path ? std::string(path) : "";
}
