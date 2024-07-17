#include <string>
#include <memory>

class InferenceInterface
{
public:
    virtual ~InferenceInterface() = default;
    virtual std::string getImageCaption(const std::string& image_path) = 0;
    virtual void loadModel() = 0;
protected:
    std::string m_collection;
};