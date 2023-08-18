import React, {useState} from 'react'
import "./Caption.css";
import { useLocation, useNavigate } from 'react-router-dom';
import Typed from 'typed.js';
import Navbar from '../Navbar/Navbar';

const Caption = () => {
    const el = React.useRef(null);
    //Type Animation
    React.useEffect(() => {
        const typed = new Typed(el.current, {
          strings: [state.caption],
          typeSpeed: 5,
          showCursor: false,
        });
        return () => {
          // Destroy Typed instance during cleanup to stop animation
          typed.destroy();
        };
      }, []);
    const navigate = useNavigate();
    const [copied, setCopied]=useState(false);
    const { state } = useLocation();
    const handleReupload = () => {
        navigate('/uploadfile') ;// Go back two pages
      };
    const address = state?.address
    const memory = state?.context
    const file = state?.file_name
    const handleRegenerate = () => {
        navigate('/generatecaption', {state:{ memory, address, file}}); // Should only go back 1 page
    };
    const handleCopy = () => { // To handle Copy text Feature
        navigator.clipboard.writeText(el.current.innerHTML);
        setCopied(true);
        setTimeout(()=>{
            setCopied(false);
        }, 3000);
    };

    
    const fileExtension = state?.file_path;
    const fileType = fileExtension.includes('mp4') || fileExtension.includes('mov') || fileExtension.includes('quicktime') || fileExtension.includes('avi')
        ? 'video'
        : 'image';

    

  return (

    <>
    <div>
        <Navbar flag={true}/>
        <section>
        <div className="content">
            <div className="innerContent-page3">
                <div className='innerContent-div'> 
                    <div className='text' >
                        <p className="steps" >Share Your Caption</p>
                        <div className='generated-caption'>
                          <div className="imgBx">
                              {fileType === "video" ? (
                                  <video controls className="cover">
                                      <source src={state?.file_path}></source>
                                  </video>
                              ) : (
                                  <img src={state?.file_path}  alt="" className='cover' />
                              )}
                          </div>
                            <p className="textarea caption" contentEditable="true" ref={el} ></p>
                        </div>
                        <div className="utilities">
                            <button className='btn-reupload' onClick={handleReupload}>Reupload <i className="fa-solid fa-cloud-arrow-up"></i></button>
                            <button className='btn-regenerate' onClick={handleRegenerate} >Regenerate <i className="fa-solid fa-arrows-rotate"></i></button>
                            <button className='btn-copy' onClick={handleCopy}>Copy <i className="fa-solid fa-copy"></i></button>
                        </div>
                        {copied && <p className="copy-text">Caption Copied Successfully!</p>}
                    </div>
                    <div>
                    </div>
                </div>
                
           </div>
           

        </div>
        <div className="footer-page3">
        </div>
        </section>
        
        
    </div>
   
    </>
  )
       
   
   

}

export default Caption