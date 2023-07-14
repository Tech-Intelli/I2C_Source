import React, {useState} from 'react';
import { Platform, View, Text, TextInput ,TouchableOpacity, Button, GestureResponderEvent, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
export default function Login(props: { navigation: { navigate: (arg0: string) => void; }; }) {
  const [email, setEmail] = useState("");  
  const [password, setPassword] = useState("");  
  const [error, setError] = useState(false);
  const [errorText, setErrorText] = useState('');
  const handleSignIn = async()=>{
    if (!email || !password)
    {
        setError(true);
        setErrorText('Please enter all fields');
    }
    else
    {
        setError(false);
        const body = {
          email: email,
          password: password
        };
        await axios
          .post('http://192.168.178.54:9000/login_user', body)
          .then((res: any) => {
            
            setEmail('');
            setPassword('');
            props.navigation.navigate("Upload")
          })
          .catch((err: any) => {
            console.log(err);
          });
    }
  }

  const handleGuestLogin = async () => {
    try {
      const response = await axios.post('http://192.168.178.54:9000/login_as_guest');
      await AsyncStorage.setItem('token', response.data.token);
      props.navigation.navigate("Upload");
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <View style={(Platform.OS == 'android')?styles_android.view: styles_ios.view}>
        <View style = {(Platform.OS == 'android')?styles_android.sign_in_components: styles_ios.sign_in_components}>
            <Text style={(Platform.OS == 'android')?styles_android.sign_in_text: styles_ios.sign_in_text}>Email</Text>
            <TextInput keyboardType="email-address" autoCapitalize="none" style={(Platform.OS == 'android')?styles_android.sign_in: styles_ios.sign_in} placeholder='Enter Email' placeholderTextColor="#E9A9CC" value={email} onChangeText={(text)=>{setEmail(text)}}/>
        </View>
        <View style = {(Platform.OS == 'android')?styles_android.sign_in_components: styles_ios.sign_in_components}>
            <Text style={(Platform.OS == 'android')?styles_android.sign_in_text: styles_ios.sign_in_text}>Password</Text>
            <TextInput style={(Platform.OS == 'android')?styles_android.sign_in: styles_ios.sign_in} placeholder='Enter Password' placeholderTextColor="#E9A9CC" secureTextEntry={true} value={password} onChangeText={(text)=>{setPassword(text)}} />
            <Text style = {(Platform.OS == 'android')?styles_android.forgot: styles_ios.forgot} onPress={()=>{props.navigation.navigate("Forgot")}}>Forgot Password?</Text>
        </View>
        {error? <Text style = {(Platform.OS == 'android')?styles_android.error_text: styles_ios.error_text}>{errorText}</Text>: null}
        <TouchableOpacity style={(Platform.OS == 'android')?styles_android.login_button: styles_ios.login_button} onPress={handleSignIn}>
            <Text style={(Platform.OS == 'android')?styles_android.login_buttonText: styles_ios.login_buttonText}>Sign In</Text>
        </TouchableOpacity>
        <TouchableOpacity style={(Platform.OS == 'android')?styles_android.login_button: styles_ios.login_button} onPress={() => { props.navigation.navigate("Home") }}>
            <Text style={(Platform.OS == 'android')?styles_android.login_buttonText: styles_ios.login_buttonText}>Continue as Guest</Text>
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
    sign_in: {
        borderBottomWidth: 3,
        borderBottomColor: '#8121D7',
        marginHorizontal: 20,
        paddingHorizontal: 10,
        color: '#E9FDFF'
    },
    sign_in_text:{
        marginVertical:10,
        marginHorizontal: 30,
        fontSize: 20,
        fontFamily: 'Source Sans Pro',
        fontWeight: 'bold',
        color: '#E9A9CC'
    },
    sign_in_components: {
        margin: 10,
        padding: 10,
        paddingBottom: 5,
        marginBottom: 20
    },
    login_button:{
        marginHorizontal: 20,
        marginTop:30,
        marginBottom: 20,
        padding: 10,
        backgroundColor: '#8121D7',
        borderRadius: 30
    },
    login_buttonText:{
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
    options_text_register: {
        textDecorationLine: 'underline',
        textDecorationColor: '#E9A9CC'
    },
    forgot:{
        fontSize: 16,
        marginVertical:10,
        marginHorizontal: 30,
        fontFamily: 'Source Sans Pro',
        color:'#E9A9CC',
        textAlign: 'right'
    },
    error_text:{
        fontSize: 18,
        color: 'red',
        fontFamily: 'Source Sans Pro',
        fontWeight: "700",
        marginHorizontal:30,
    }
});

const styles_ios = StyleSheet.create({
    view:{
        backgroundColor: '#111111',
        flex:1,
    },
    sign_in: {
        borderBottomWidth: 3,
        borderBottomColor: '#8121D7',
        marginHorizontal: 20,
        paddingHorizontal: 10,
        color: '#E9FDFF'
    },
    sign_in_text:{
        marginVertical:10,
        marginHorizontal: 30,
        fontSize: 20,
        fontFamily: 'Source Sans Pro',
        fontWeight: 'bold',
        color: '#E9A9CC'
    },
    sign_in_components: {
        margin: 10,
        padding: 10,
        paddingBottom: 5,
        marginBottom: 20
    },
    login_button:{
        marginHorizontal: 20,
        marginTop:30,
        marginBottom: 20,
        padding: 10,
        backgroundColor: '#8121D7',
        borderRadius: 30
    },
    login_buttonText:{
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
    options_text_register: {
        textDecorationLine: 'underline',
        textDecorationColor: '#E9A9CC'
    },
    forgot:{
        fontSize: 16,
        marginVertical:10,
        marginHorizontal: 30,
        fontFamily: 'Source Sans Pro',
        color:'#E9A9CC',
        textAlign: 'right'
    },
    error_text:{
        fontSize: 18,
        color: 'red',
        fontFamily: 'Source Sans Pro',
        fontWeight: "700",
        marginHorizontal:30,
    }
});