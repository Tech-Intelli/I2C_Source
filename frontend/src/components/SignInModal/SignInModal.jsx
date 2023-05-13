import React,{useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import "./SignModal.css"
import facebook from "./facebook.svg";
import instagram from "./instagram.svg";
import twitter from "./twitter.svg";
import linkedin from "./linkedin.svg";
import { Link } from 'react-router-dom';
export function SignInModal(props) {

  const [login,setlogin]  = useState(false);
  return (
    <>
      <Modal
        className='SignModal'
        show={props.show}
        onHide={props.handleClose}
        // backdrop="static"
        keyboard={false}
      >
        
          {!login?<div>
          <Modal.Title>Sign Up</Modal.Title>
          <input placeholder='Enter email or mobile'/>
          <input placeholder='Enter Password' type = "password"/>
          <input placeholder='Confirm Password' type="password"/>
          <button className="btn-style modal-btn-btn" >Sign Up</button>
          <hr class="hr-text" data-content="OR"/>
          <div className='socialHandles'>
          <img src ={facebook} alt= "facebook"></img>
          <img src ={instagram} alt = "instagram"></img>
          <img src ={twitter} alt ="twitter"></img>
          <img src ={linkedin} alt ="linkedin"></img>
          </div>
          <div className='modalFooter'>
              <p>Already a user? <span onClick={()=>setlogin(!login)}>LOGIN</span></p>
          </div>

          
          </div>:
          <div>
          <Modal.Title>Sign In</Modal.Title>
          <input placeholder='Enter email or mobile'/>
          <input placeholder='Enter Password' type = "password"/>
          <Link to = "/uploadfile"><button className="btn-style modal-btn-btn" >Login</button></Link>
          <hr class="hr-text" data-content="OR"/>
          <div className='socialHandles'>
          <img src ={facebook} alt= "facebook"></img>
          <img src ={instagram} alt = "instagram"></img>
          <img src ={twitter} alt ="twitter"></img>
          <img src ={linkedin} alt ="linkedin"></img>
          </div>
          <div className='modalFooter'>
              <p>Not a user? <span onClick={()=>setlogin(!login)}>SIGN UP</span></p>
          </div>

          
          </div>
          }
         
        
         
        
        
        {/* <Modal.Body>
          I will not close if you click outside me. Don't even try to press
          escape key.
        </Modal.Body> */}
        {/* <Modal.Footer>
          <Button variant="secondary" onClick={props.handleClose}>
            Close
          </Button>
          <Button variant="primary">Understood</Button>
        </Modal.Footer> */}
      </Modal>
    </>
  );
}

