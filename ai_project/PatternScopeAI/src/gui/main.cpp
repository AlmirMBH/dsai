#include "Application.h"
#include <gui/WinMain.h>

int main(int argc, const char * argv[])
{
    Application app(argc, argv);
    app.init("EN");
    return app.run();
}

