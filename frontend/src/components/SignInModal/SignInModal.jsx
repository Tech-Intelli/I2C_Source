import React,{useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import "./SignModal.css"
import facebook from "../assets/icons/facebook.svg";
import instagram from "../assets/icons/instagram.svg";
import twitter from "../assets/icons/twitter.svg";
import linkedin from "../assets/icons/linkedin.svg";
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";
import {Circles} from "react-loader-spinner"
export function SignInModal(props) {
  const navigate =useNavigate();

  const [login,setlogin]  = useState(false);
  const [email,setEmail]= useState();
  const [password,setPassword] = useState();
  const [confirmPass,setConfirmPass] =useState();
  const [error,setError]  = useState(false);
  const [ErrorText,setErrorText]  = useState("");
  const [success,setsuccess] = useState();
  const [loading,setLoading] = useState(false);

  const handleLogin = async ()=>{
    if(!email|| !password){
      console.log("Please Enter All Fields");
    }else{
      setLoading(true);
      const body ={
        email:email,
        password:password
      }
      await axios.post("http://localhost:9000/login_user",body).then(res=>{
        setLoading(false);
        localStorage.setItem("token",res.data.token);
        navigate("/uploadfile");
        
      }).catch(err=>{
        console.log(err);
      });
    }
  }

  const handleSignUp = async () =>{
    if(!email || !password){
      setError(true);
      setErrorText("Please Enter All Fields ")
    }else{
      setError(false);
      if(password !== confirmPass){
        setError(true);
        setErrorText("Passwords Don't Match!");
      }else{
        setLoading(true);
        setError(false);
         const body = {
           email: email,
           password:password
         };
         await axios.post("http://localhost:9000/register_user",body).then(res=>{
            setsuccess("User Registered Successfully! Please verify Your Email To Login!");
            setLoading(false);
            setEmail();
            setPassword();
            setConfirmPass();
         }).catch(err=>{
            console.log(err);
         });

      }
     
    }

  }
  return (
    <>
      <Modal
        className="SignModal"
        show={props.show}
        onHide={props.handleClose}
        // backdrop="static"
        keyboard={false}
      >
        {!login ? (
          <div>
            <Modal.Title>
              Sign Up {error ? <p className="errorText">{ErrorText}</p> : null}
            </Modal.Title>

            <input
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              placeholder="Enter Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <input
              placeholder="Confirm Password"
              type="password"
              value={confirmPass}
              onChange={(e) => setConfirmPass(e.target.value)}
            />
            {!success ? (
              loading ? (
                <>
                  <div className="spinners">
                    <Circles
                      height="50"
                      width="50"
                      color="#1c4042"
                      ariaLabel="circles-loading"
                      wrapperStyle={{}}
                      wrapperClass=""
                      visible={true}
                    ></Circles>
                  </div>
                </>
              ) : (
                <button
                  className="btn-style modal-btn-btn"
                  onClick={handleSignUp}
                >
                  Sign Up
                </button>
              )
            ) : (
              <p className="success">{success}</p>
            )}
            <hr class="hr-text" data-content="OR" />
            <div className="socialHandles">
              <img src={facebook} alt="facebook"></img>
              <img src={instagram} alt="instagram"></img>
              <img src={twitter} alt="twitter"></img>
              <img src={linkedin} alt="linkedin"></img>
            </div>
            <div className="modalFooter">
              <p>
                Already a user?{" "}
                <span onClick={() => setlogin(!login)}>LOGIN</span>
              </p>
            </div>
          </div>
        ) : (
          <div>
            <Modal.Title>Sign In</Modal.Title>
            <input
              placeholder="Enter email or mobile"
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              placeholder="Enter Password"
              type="password"
              onChange={(e) => {
                setPassword(e.target.value);
              }}
            />
              {loading ? (
                <>
                  <div className="spinners">
                    <Circles
                      height="50"
                      width="50"
                      color="#1c4042"
                      ariaLabel="circles-loading"
                      wrapperStyle={{}}
                      wrapperClass=""
                      visible={true}
                    ></Circles>
                  </div>
                </>
              ) : (
                <button
                  className="btn-style modal-btn-btn"
                  onClick={handleLogin}
                >
                  Login
                </button>
              )}
            <hr class="hr-text" data-content="OR" />
            <div className="socialHandles">
              <img src={facebook} alt="facebook"></img>
              <img src={instagram} alt="instagram"></img>
              <img src={twitter} alt="twitter"></img>
              <img src={linkedin} alt="linkedin"></img>
            </div>
            <div className="modalFooter">
              <p>
                Not a user?{" "}
                <span onClick={() => setlogin(!login)}>SIGN UP</span>
              </p>
            </div>
          </div>
        )}  
      </Modal>
    </>
  );
}

