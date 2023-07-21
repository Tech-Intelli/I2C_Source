import React, {useState} from 'react';
import { Platform , Alert, View, Text, TextInput ,TouchableOpacity, StyleSheet } from 'react-native';
import axios from 'axios';
export default function Register(props: { navigation: { navigate: (arg0: string) => void; }; }) {
  const [email, setEmail] = useState("");  
  const [password, setPassword] = useState("");  
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(false);
  const [errorText, setErrorText] = useState('');
  const handleResetPassword = async()=>{
    if (!email || !password || !confirmPassword)
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
          username: email,
          password: password
        };
        await axios
          .post('http://192.168.0.159:9000/forget_password', body)
          .then((res: any) => {
            
            setEmail('');
            setPassword('');
            setConfirmPassword('');
            showAlert("Password changed successfully! You can now login with the new password.");
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
        { text: 'OK', onPress: () => props.navigation.navigate("Login") }
      ],
      { cancelable: false } 
    );
  };
  return (
    <View style={(Platform.OS == 'android')?styles_android.view:styles_ios.view}>
        <View style = {(Platform.OS == 'android')?styles_android.forgot_components: styles_ios.forgot_components}>
            <Text style={(Platform.OS == 'android')?styles_android.forgot_text: styles_ios.forgot_text}>Email</Text>
            <TextInput keyboardType="email-address" autoCapitalize="none" style={(Platform.OS == 'android')?styles_android.forgot: styles_ios.forgot} placeholder='Enter Email' placeholderTextColor="#E9A9CC" value={email} onChangeText={(text)=>{setEmail(text)}}/>
        </View>
        <View style = {(Platform.OS == 'android')?styles_android.forgot_components: styles_ios.forgot_components}>
            <Text style={(Platform.OS == 'android')?styles_android.forgot_text: styles_ios.forgot_text}>New Password</Text>
            <TextInput style={(Platform.OS == 'android')?styles_android.forgot: styles_ios.forgot} placeholder='Enter Password' placeholderTextColor="#E9A9CC" secureTextEntry={true} value={password} onChangeText={(text)=>{setPassword(text)}} />
        </View>
        <View style = {(Platform.OS == 'android')?styles_android.forgot_components: styles_ios.forgot_components}>
            <Text style={(Platform.OS == 'android')?styles_android.forgot_text: styles_ios.forgot_text}>Confirm Password</Text>
            <TextInput style={(Platform.OS == 'android')?styles_android.forgot: styles_ios.forgot} placeholder='Confirm  Password' placeholderTextColor="#E9A9CC" secureTextEntry={true} value={confirmPassword} onChangeText={(text)=>{setConfirmPassword(text)}} />
        </View>
        <TouchableOpacity style={(Platform.OS == 'android')?styles_android.reset_button: styles_ios.reset_button} onPress={handleResetPassword}>
            <Text style={(Platform.OS == 'android')?styles_android.reset_buttonText: styles_ios.reset_buttonText}>Reset Password</Text>
        </TouchableOpacity>
        <View style={(Platform.OS == 'android')?styles_android.options: styles_ios.options}>
            <Text style={(Platform.OS == 'android')?styles_android.options_text: styles_ios.options_text}>
                Not a user?
                &nbsp;<Text style= {(Platform.OS == 'android')?styles_android.options_text_register: styles_ios.options_text_register} onPress={()=>{props.navigation.navigate("Register")}}>Sign Up</Text>
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
    forgot: {
        marginHorizontal: 20,
        borderBottomWidth: 3,
        borderBottomColor: '#8121D7',
        paddingHorizontal: 10,
        color: '#E9FDFF'
    },
    forgot_text:{
        marginVertical:10,
        marginHorizontal: 30,
        fontSize: 20,
        fontFamily: 'Josefin Sans',
        fontWeight: 'bold',
        color: '#E9A9CC'
    },
    forgot_components: {
        margin: 10
    },
    reset_button:{
        marginHorizontal:25,
        marginTop:30,
        marginBottom: 20,
        padding: 10,
        backgroundColor: '#8121D7',
        borderRadius: 30
    },
    reset_buttonText:{
        color: '#E9FDFF',
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
    options_text_register: {
        textDecorationLine: 'underline',
        textDecorationColor: '#E9A9CC'
    }
});

const styles_ios = StyleSheet.create({
    view:{
        backgroundColor: '#111111',
        flex:1,
    },
    forgot: {
        marginHorizontal: 20,
        borderBottomWidth: 3,
        borderBottomColor: '#8121D7',
        paddingHorizontal: 10,
        color: '#E9FDFF'
    },
    forgot_text:{
        marginVertical:10,
        marginHorizontal: 30,
        fontSize: 20,
        fontFamily: 'Josefin Sans',
        fontWeight: 'bold',
        color: '#E9A9CC'
    },
    forgot_components: {
        margin: 10
    },
    reset_button:{
        marginHorizontal:25,
        marginTop:30,
        marginBottom: 20,
        padding: 10,
        backgroundColor: '#8121D7',
        borderRadius: 30
    },
    reset_buttonText:{
        color: '#E9FDFF',
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
    options_text_register: {
        textDecorationLine: 'underline',
        textDecorationColor: '#E9A9CC'
    }
});