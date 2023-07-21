import React, {useState} from 'react';
import { Alert, View, Text, TextInput ,TouchableOpacity, StyleSheet, Platform } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { REACT_APP_BACKEND_URL } from '@env';


export default function Register(props: { navigation: {
    setOptions(arg0: { headerRight: () => React.JSX.Element; title: string; }): unknown; navigate: (arg0: string) => void; 
}; }) {
  const [email, setEmail] = useState("");  
  const [password, setPassword] = useState("");  
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(false);
  const [errorText, setErrorText] = useState('');
  const handleSignUp = async()=>{
    if (!email || !password)
    {
        setError(true);
        setErrorText('Please enter all fields');
    }
    else if (password !== confirmPassword)
    {
        setError(true);
        setErrorText("Passwords don't match!");
    }
    else
    {
        
        setError(false);
        const body = {
          email: email,
          password: password
        };
        await axios
          .post(`${REACT_APP_BACKEND_URL}/register_user`, body)
          .then((res: any) => {
            
            setEmail('');
            setPassword('');
            setConfirmPassword('');
            showAlert("User registered successfully! Please verify your email to login!");
          })
          .catch((err: any) => {
            console.log(err);
          });
      }
  }

  const showAlert = (msg: string | undefined) => {
    Alert.alert(
      'Success',     
      msg,
      [
        { text: 'OK' }
      ],
      { cancelable: false } 
    );
  };

  const handleGuestLogin = async () => {
    
    console.log("Signing Up")
    try {
      const response = await axios.post(`${REACT_APP_BACKEND_URL}/login_as_guest`);
      console.log("Signing Up")
      await AsyncStorage.setItem('token', response.data.token);
      props.navigation.navigate("Upload");
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <View style={(Platform.OS == 'android')?styles_android.view: styles_ios.view}>
        <View style = {(Platform.OS == 'android')?styles_android.sign_up_components: styles_ios.sign_up_components}>
            <Text style={(Platform.OS == 'android')?styles_android.sign_up_text : styles_ios.sign_up_text }>Email</Text>
            <TextInput keyboardType="email-address" autoCapitalize="none" style={(Platform.OS == 'android')? styles_android.sign_up: styles_ios.sign_up} placeholder='Enter Email'  placeholderTextColor="#E9A9CC" value={email} onChangeText={(text)=>{setEmail(text)}}/>
        </View>
        <View style = {(Platform.OS == 'android')?styles_android.sign_up_components: styles_ios.sign_up_components}>
            <Text style={(Platform.OS == 'android')?styles_android.sign_up_text: styles_ios.sign_up_text}>Password</Text>
            <TextInput style={(Platform.OS == 'android')?styles_android.sign_up: styles_ios.sign_up} placeholder='Enter Password' placeholderTextColor="#E9A9CC" secureTextEntry={true} value={password} onChangeText={(text)=>{setPassword(text)}} />
        </View>
        <View style = {(Platform.OS == 'android')?styles_android.sign_up_components: styles_ios.sign_up_components}>
            <Text style={(Platform.OS == 'android')?styles_android.sign_up_text: styles_ios.sign_up_text}>Confirm Password</Text>
            <TextInput style={(Platform.OS == 'android')?styles_android.sign_up: styles_ios.sign_up} placeholder='Confirm  Password' placeholderTextColor="#E9A9CC" secureTextEntry={true} value={confirmPassword} onChangeText={(text)=>{setConfirmPassword(text)}} />
        </View>
        {error? <Text style = {(Platform.OS == 'android')?styles_android.error_text: styles_ios.error_text}>{errorText}</Text>: null}        
        <TouchableOpacity style={(Platform.OS == 'android')?styles_android.register_button:styles_ios.register_button} onPress={handleSignUp}>
            <Text style={(Platform.OS == 'android')?styles_android.register_buttonText : styles_ios.register_buttonText}>Sign Up</Text>
        </TouchableOpacity>
        <TouchableOpacity style={(Platform.OS == 'android')?styles_android.register_button: styles_ios.register_button} onPress={handleGuestLogin}>
            <Text style={(Platform.OS == 'android')?styles_android.register_buttonText : styles_ios.register_buttonText}>Continue as Guest</Text>
        </TouchableOpacity>
        <View style={(Platform.OS == 'android')?styles_android.options: styles_ios.options}>
            <Text style={(Platform.OS == 'android')?styles_android.options_text: styles_ios.options_text}>
                Already a user?
                &nbsp;<Text style= {(Platform.OS == 'android')?styles_android.options_text_login: styles_ios.options_text_login} onPress={()=>{props.navigation.navigate("Login")}}>Sign In</Text>
            </Text>
        </View>
    </View>
    
  )
}

const styles_android = StyleSheet.create({
    view:{
        backgroundColor: '#111111',
        flex:1,
    },
    sign_up: {
        marginHorizontal: 20,
        borderBottomWidth: 3,
        borderBottomColor: '#8121D7',
        paddingHorizontal: 10,
        marginBottom: 10
    },
    sign_up_text:{
        marginVertical:10,
        marginHorizontal: 30,
        fontSize: 20,
        fontFamily: 'Source Sans Pro',
        fontWeight: 'bold',
        color: '#E9FDFF'
    },
    sign_up_components: {
        margin: 10,
    },
    register_button:{
        marginHorizontal:20,
        marginTop:30,
        marginBottom: 20,
        padding: 10,
        backgroundColor: '#8121D7',
        borderRadius: 30
    },
    register_buttonText:{
        color: 'white',
        fontSize: 16,
        textAlign: 'center',
    },
    options:{
        marginHorizontal: 20
    },
    options_text:{
        fontSize: 20,
        color: '#E9A9CC',
        textAlign: 'center'
    },
    options_text_login: {
        textDecorationLine: 'underline'
    },
    error_text:{
        fontSize: 18,
        color: 'red',
        fontFamily: 'Source Sans Pro',
        fontWeight: "700",
        marginHorizontal:30,
    },
    logoutIcon: {
        height: 30,
        width: 30,
        marginHorizontal: 5,
      }
});
const styles_ios = StyleSheet.create({
  view:{
      backgroundColor: '#111111',
      flex:1,
  },
  sign_up: {
      marginHorizontal: 20,
      borderBottomWidth: 3,
      borderBottomColor: '#8121D7',
      paddingHorizontal: 10,
      marginBottom: 10
  },
  sign_up_text:{
      marginVertical:10,
      marginHorizontal: 30,
      fontSize: 20,
      fontFamily: 'Source Sans Pro',
      fontWeight: 'bold',
      color: '#E9FDFF'
  },
  sign_up_components: {
      margin: 10,
  },
  register_button:{
    marginHorizontal:20,
    marginTop:30,
    marginBottom: 20,
    padding: 10,
    width: "90%",
    backgroundColor: '#8121D7',
    borderRadius: 30
},
  register_buttonText:{
      color: 'white',
      fontSize: 16,
      textAlign: 'center',
  },
  options:{
      marginHorizontal: 20
  },
  options_text:{
      fontSize: 20,
      color: '#E9A9CC',
      textAlign: 'center'
  },
  options_text_login: {
      textDecorationLine: 'underline'
  },
  error_text:{
      fontSize: 18,
      color: 'red',
      fontFamily: 'Source Sans Pro',
      fontWeight: "700",
      marginHorizontal:30,
  },
  logoutIcon: {
    height: 30,
    width: 30,
    marginHorizontal: 5,
  }
});