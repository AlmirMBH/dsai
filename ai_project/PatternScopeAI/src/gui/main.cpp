#include "Application.h"
#include "core/ResourcePath.h"
#include <gui/WinMain.h>

int main(int argc, const char * argv[])
{
    ResourcePath::init(argc > 0 ? argv[0] : "PatternVision");
    Application app(argc, argv);
    app.init("EN");
    return app.run();
}
