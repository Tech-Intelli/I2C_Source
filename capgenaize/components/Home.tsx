import * as React from 'react';
import { Platform,View, Text, Image,TouchableOpacity, Button, GestureResponderEvent, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

export default function Home(props: { navigation: { navigate: (arg0: string) => ((event: GestureResponderEvent) => void) | undefined; }; }) {

  
  return (
    <View style={(Platform.OS == 'android')?styles_android.main_body: styles_ios.main_body}>
      <View style={(Platform.OS == 'android')? styles_android.content : styles_ios.content}>
        <Image style={(Platform.OS == 'android')? styles_android.intro_image: styles_ios.intro_image} source={require('../assets/landing-page-image-1.png')} />
        <Text style={(Platform.OS == 'android')? styles_android.intro_text: styles_ios.intro_text }>CapGenAIze</Text>
        <Text style={(Platform.OS == 'android')? styles_android.intro_subtext:styles_ios.intro_subtext }>Crafting Captions with AI Precision</Text>
      </View>
      <TouchableOpacity style={(Platform.OS == 'android')? styles_android.button: styles_ios.button} onPress={() => { props.navigation.navigate("Register") }}>
        <Text style={(Platform.OS == 'android')? styles_android.buttonText: styles_ios.buttonText}>Start Now</Text>
    </TouchableOpacity>
    </View>
  );
}

const styles_android = StyleSheet.create({
  main_body: {
    backgroundColor: '#111111',
    fontFamily: 'Source Sans Pro',
    flex: 1,
    justifyContent: 'center',
  },
  content: {
    alignItems: 'center',
  },
  intro_text: {
    marginLeft: 10,
    marginRight: 10,
    fontSize: 36,
    fontFamily: 'Source Sans Pro',
    fontWeight: '600',
    flexWrap: 'wrap',
    textAlign: 'center',
    color: '#E9FDFF',
  },
  highlight_text: {
    color: '#BD6896',
  },
  intro_subtext: {
    color: '#E9FDFF',
    fontSize: 20,
    fontFamily: 'Source Sans Pro',
    fontWeight: '100',
    marginBottom: 20
  },
  intro_image: {
    height: 300,
    width: 300,
    alignSelf: 'center',
  },
  button:{
    marginHorizontal:25,
    marginVertical:15,
    padding: 10,
    backgroundColor: '#8121D7',
    borderRadius: 30
  },
  buttonText: {
    color:'#E9FDFF',
    fontSize: 16,
    textAlign: 'center',
  },
});

const styles_ios = StyleSheet.create({
  main_body: {
    backgroundColor: '#111111',
    fontFamily: 'Source Sans Pro',
    flex: 1,
    justifyContent: 'center',
  },
  content: {
    alignItems: 'center',
  },
  intro_text: {
    marginLeft: 10,
    marginRight: 10,
    fontSize: 36,
    fontFamily: 'Source Sans Pro',
    fontWeight: '600',
    flexWrap: 'wrap',
    textAlign: 'center',
    color: '#E9FDFF',
  },
  highlight_text: {
    color: '#BD6896',
  },
  intro_subtext: {
    color: '#E9FDFF',
    fontSize: 20,
    fontFamily: 'Source Sans Pro',
    fontWeight: '100',
    marginBottom: 20
  },
  intro_image: {
    height: 300,
    width: 300,
    alignSelf: 'center',
  },
  button:{
    marginHorizontal:15,
    marginVertical:10,
    padding: 10,
    backgroundColor: '#8121D7',
    borderRadius: 30
  },
  buttonText: {
    color:'#111111',
    fontSize: 16,
    textAlign: 'center',
  },
});

