#include <string>
#include <memory>

/**
 * @brief Class representing an interface for inference operations.
 * 
 * This class provides methods for getting image captions and loading models for inference.
 * 
 * Public Methods:
 *  - std::string getImageCaption(const std::string& image_path): Retrieves a caption for the specified image.
 *  - void loadModel(): Loads the model for inference.
 * 
 * Protected Attributes:
 *  - std::string m_collection: A string representing the collection used by the interface.
 */
class InferenceInterface
{
public:
    virtual ~InferenceInterface() = default;
    virtual std::string getImageCaption(const std::string& image_path) = 0;
    virtual void loadModel() = 0;
protected:
    std::string m_collection;
};