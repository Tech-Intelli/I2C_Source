import React, { useState, useLayoutEffect } from 'react';
import { Alert,AlertButton,View, Image, Text, TouchableOpacity, StyleSheet, ScrollView, Platform, Modal} from 'react-native';
import { RootStackParamList } from '../App';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import Slider from '@react-native-community/slider';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';



type GenerateProps = NativeStackScreenProps<RootStackParamList, 'Generate'>;
export default function Generate({ route, navigation }: GenerateProps) {
  const { memory,address, filename, filenameURI} = route.params;
  //const token1 = localStorage.getItem('token')
  const [selectedSize, setSelectedSize] = useState('small');
  const styleOption = ['cool', 'professional', 'artistic', 'poetic', 'poetry']
  const [Style,setStyle] = useState(0);
  const [selectedStyle, setSelectedStyle] = useState(styleOption[0]);
  const [hashtags, setHashtags] = useState(0);
  const [selected, setSelected] = useState(0);
  const toneOptions = ['casual', 'humorous', 'inspirational','conversational', 'educational', 'storytelling','sentimental'];
  const [tone, setTone] = useState(toneOptions[0]);
  const [socials, setSocials]=useState('instagram');
  const [loading, setLoading] = useState(false);

  

  const handleSizePress = (size: string) => {
    setSelectedSize(size === selectedSize ? '' : size);
  };

  const handleStylePress = (style: string) => {
    setSelectedStyle(style === selectedStyle ? '' : style);
  };

  const renderImage = (size: string) => {
    if (selectedSize === size) {
      return (
        <Image
          style={(Platform.OS == 'android')?styles_android.imageActive: styles_ios.imageActive}
          source={require('../assets/caption_size_active.png')}
        />
      );
    }
    return (
      <Image
        style={(Platform.OS == 'android')?styles_android.image: styles_ios.image}
        source={require('../assets/caption_size.png')}
      />
    );
  };


  const handlePress = async()=>{
    //navigation.push("Caption");
    setLoading(true);

    let file_name = null;
    if(filename)
    {
      file_name = filename.name;
    }
    const token = await AsyncStorage.getItem("token");
    await axios.get(`http://192.168.0.159:9000/generate_image_video_caption?caption_size=${selectedSize}&context=${memory}&style=${selectedStyle}&num_hashtags=${hashtags}&tone=${tone}&social_media=${socials}&file_name=${JSON.stringify(filename)}&address=${address}`,{
      headers:{
          Authorization: `Bearer ${token}`
      },
      withCredentials: true
  }).then(res=>{
    navigation.push("Caption",{caption: res.data.Caption, filename:filenameURI});
    setLoading(false);
}).catch((err) => {
  console.log(err);
});
}
const handleLogout = async () => {
  const logoutAlertOptions: AlertButton[] = [
    { text: 'Cancel', style: 'cancel' },
    {
      text: 'OK',
      onPress: async () => {
        console.log('Logout');
        await axios
          .post('http://192.168.0.159:9000/logout_user')
          .then((res) => {
            // Perform any additional actions after successful logout
            navigation.popToTop()
          })
          .catch((error) => {
            // Handle error if logout fails
            console.log(error);
          });
      },
    },
  ];

  Alert.alert('Logout', 'Are you sure you want to logout?', logoutAlertOptions, {
    cancelable: false,
  });
};
useLayoutEffect(() => {
  navigation.setOptions({
    headerRight: () => (
      <TouchableOpacity onPress={handleLogout}>
        <Image
          source={require('../assets/logout.png')}
          style={
            Platform.OS === 'android'
              ? styles_android.logoutIcon
              : styles_ios.logoutIcon
          }
        />
      </TouchableOpacity>
    ),
    title: 'Choose Caption',
  });
}, [navigation]);
  return (
    <View style={(Platform.OS == 'android')?styles_android.page: styles_ios.page}>
      <ScrollView>
        <Text style={(Platform.OS == 'android')?styles_android.input_header: styles_ios.input_header}>Caption Size</Text>
        <View style={(Platform.OS == 'android')?styles_android.imageContainer: styles_ios.imageContainer}>
          <View style={(Platform.OS == 'android')?styles_android.buttonContainer: styles_ios.buttonContainer}>
            <TouchableOpacity
              onPress={() => handleSizePress('small')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSize: styles_ios.touchableSize,
                selectedSize === 'small' && ((Platform.OS == 'android')?styles_android.activeSize: styles_ios.activeSize)
              ]}
            >
            <Text style={[(Platform.OS == 'android')?styles_android.buttonText: styles_ios.buttonText, selectedSize === 'small' && ((Platform.OS == 'android')?styles_android.buttonTextActive: styles_ios.buttonTextActive)  ]}>Small</Text>
            </TouchableOpacity>
          </View>
          <View style={(Platform.OS == 'android')?styles_android.buttonContainer: styles_ios.buttonContainer}>
          <TouchableOpacity
              onPress={() => handleSizePress('medium')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSize: styles_ios.touchableSize,
                selectedSize === 'medium' && ((Platform.OS == 'android')?styles_android.activeSize: styles_ios.activeSize)
              ]}
            >
            <Text style={[(Platform.OS == 'android')?styles_android.buttonText: styles_ios.buttonText, selectedSize === 'medium' && ((Platform.OS == 'android')?styles_android.buttonTextActive: styles_ios.buttonTextActive)  ]}>Medium</Text>
            </TouchableOpacity>
          </View>
          <View style={(Platform.OS == 'android')?styles_android.buttonContainer: styles_ios.buttonContainer}>
          <TouchableOpacity
              onPress={() => handleSizePress('large')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSize: styles_ios.touchableSize,
                selectedSize === 'large' && ((Platform.OS == 'android')?styles_android.activeSize: styles_ios.activeSize)
              ]}
            >
            <Text style={[(Platform.OS == 'android')?styles_android.buttonText: styles_ios.buttonText, selectedSize === 'large' && ((Platform.OS == 'android')?styles_android.buttonTextActive: styles_ios.buttonTextActive)  ]}>Large</Text>
            </TouchableOpacity>
          </View>
        </View>

        <Text style={(Platform.OS == 'android')?styles_android.input_header: styles_ios.input_header}>Caption Style</Text>
        <View>
        <Text style={(Platform.OS == 'android')?styles_android.buttonTextRest: styles_ios.buttonTextRest}>{selectedStyle}</Text>
        <Slider
            style={(Platform.OS == 'android')?styles_android.slider: styles_ios.slider}
            minimumValue={0}
            maximumValue={4}
            minimumTrackTintColor="#8121D7"
            maximumTrackTintColor="#E9A9CC"
            thumbTintColor='#8121D7'
            step={1}
            value={Style}
            onValueChange={(value) =>{
              setStyle(value);
              setSelectedStyle(styleOption[Style]);
            }
              }
          />
          
        </View>

        <Text style={(Platform.OS == 'android')?styles_android.input_header: styles_ios.input_header}>Number of Hashtags</Text>
        <View>
        <Text style={(Platform.OS == 'android')?styles_android.buttonTextRest: styles_ios.buttonTextRest}>{hashtags}</Text>
          <Slider
            style={(Platform.OS == 'android')?styles_android.slider: styles_ios.slider}
            minimumValue={0}
            maximumValue={30}
            minimumTrackTintColor="#8121D7"
            maximumTrackTintColor="#E9A9CC"
            thumbTintColor='#8121D7'
            step={1}
            value={hashtags}
            onValueChange={(value) => setHashtags(value)}
          />
          
        </View>
        
        <Text style={(Platform.OS == 'android')?styles_android.input_header: styles_ios.input_header}>Caption Tone</Text>
        <Text style={(Platform.OS == 'android')?styles_android.buttonTextRest: styles_ios.buttonTextRest}>{tone}</Text>
        <Slider
          style={(Platform.OS == 'android')?styles_android.slider: styles_ios.slider}
          minimumValue={0}
          maximumValue={6}
          minimumTrackTintColor="#8121D7"
          maximumTrackTintColor="#E9A9CC"
          thumbTintColor='#8121D7'
          step={1}
          value={selected}
          onValueChange={(value) => {
            setSelected(value);
            setTone(toneOptions[value]);
          }}
        />
        <Text style={(Platform.OS == 'android')?styles_android.input_header: styles_ios.input_header}>Preferred Platform</Text>
        <View style={(Platform.OS == 'android')?styles_android.socialsContainer: styles_ios.socialsContainer}>
            <TouchableOpacity
              onPress={() => setSocials('facebook')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSocial: styles_ios.touchableSocial,
                socials === 'facebook' && ((Platform.OS == 'android')?styles_android.activeSocial: styles_ios.activeSocial),
              ]}
            >
              <Image source={require('../assets/facebook.png')}/>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => setSocials('instagram')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSocial: styles_ios.touchableSocial,
                socials === 'instagram' && ((Platform.OS == 'android')?styles_android.activeSocial: styles_ios.activeSocial),
              ]}
            >
              <Image source={require('../assets/instagram.png')}/>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => setSocials('linkedin')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSocial: styles_ios.touchableSocial,
                socials === 'linkedin' && ((Platform.OS == 'android')?styles_android.activeSocial: styles_ios.activeSocial),
              ]}
            >
              <Image source={require('../assets/linkedin.png')}/>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => setSocials('twitter')}
              style={[
                (Platform.OS == 'android')?styles_android.touchableSocial: styles_ios.touchableSocial,
                socials === 'twitter' && ((Platform.OS == 'android')?styles_android.activeSocial: styles_ios.activeSocial),
              ]}
            >
              <Image source={require('../assets/twitter.png')}/>
            </TouchableOpacity>
          </View>
          <TouchableOpacity style={(Platform.OS == 'android')?styles_android.generate_button: styles_ios.generate_button} onPress={handlePress}>
            <Text style={(Platform.OS == 'android')?styles_android.generate_buttonText: styles_ios.generate_buttonText}>Generate Caption</Text>
          </TouchableOpacity>
      </ScrollView>
      <Modal visible={loading} transparent>
        <View style={(Platform.OS == 'android')?styles_android.popupContainer: styles_ios.popupContainer}>
          <Image source={require('../assets/loading_page_image.png')} style={(Platform.OS == 'android')?styles_android.loaderImage: styles_ios.loaderImage}/>
          <Image source={require('../assets/loader.gif') } style={(Platform.OS == 'android')?styles_android.loaderContainer: styles_ios.loaderContainer}/>
          <Text style={(Platform.OS == 'android')?styles_android.loadingText: styles_ios.loadingText}>Generating the caption. Grab a cup of tea or coffee in the meantime!</Text>
        </View>
      </Modal>
    </View>
  );
}

const styles_android = StyleSheet.create({
  page: {
    backgroundColor: '#111111',
    flex: 1,
    padding: 10,
  },
  input_header: {
    fontFamily: 'Source Sans Pro',
    fontSize: 25,
    fontWeight: '700',
    marginTop: 20,
    marginBottom:10,
    marginHorizontal:10,
    color: '#E9A9CC'
  },
  imageContainer: {
    flexDirection: 'row',
    gap: 20,
    marginTop: 10,
    marginBottom: 20,
  },
  buttonContainer: {
    alignItems: 'center',
    marginHorizontal: 5
  },
  touchableSize: {
    backgroundColor: '#E9FDFF',
    paddingVertical:5,
    width: 100,
    borderRadius: 32,
  },
  activeSize: {
    backgroundColor: '#8121D7',
  },
  image: {
    width: 25,
    height: 25,
  },
  imageActive: {
    width: 25,
    height: 25,
  },
  buttonText: {
    color: '#111111',
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
    textAlign:'center',
    fontSize: 16,
  },
  buttonTextActive:{
    color: '#E9FDFF'
  },
  buttonTextRest: {
    marginTop: 5,
    marginHorizontal:10,
    color: '#E9A9CC',
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
    fontSize: 18,
  },
  buttonTextStyle: {
    marginTop: 5,
    color: '#1C4042',
    fontFamily: 'Source Sans Pro',
    fontSize: 12,
    textAlign: 'center',
    fontWeight: '700',
  },
  buttonTextStyleActive: {
    marginTop: 5,
    color: '#E9FDFF',
    fontFamily: 'Source Sans Pro',
    fontSize: 12,
    textAlign: 'center',
    fontWeight: '700',
  },
  touchableStyle: {
    backgroundColor: '#E9FDFF',
    width: 70,
    height: 25,
    borderRadius: 20,
  },
  activeStyle: {
    backgroundColor: '#1C4042',
    borderRadius: 20,
  },
  socialsContainer:{
    flexDirection: 'row',
    gap:20,
    marginHorizontal:5,
    marginBottom: 10
  },
  touchableSocial: {
    borderWidth: 0
  },
  activeSocial:{
    borderWidth: 3,
    borderColor: '#8121D7',
    borderRadius: 16
  },
  generate_button: {
    marginLeft: 8,
    marginRight:30,
    marginTop: 20,
    marginBottom: 20,
    padding: 10,
    backgroundColor: '#8121D7',
    borderRadius: 30,
  },
  generate_buttonText: {
    color: 'white',
    fontSize: 18,
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
    textAlign: 'center',
  },
  popupContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#111111',
  },
  loadingText: {
    color: '#E9FDFF',
    marginTop: 10,
    fontSize: 18,
    textAlign: 'center',
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
  },
  loaderContainer: {
    transform: [{scale: 0.35}]
  },
  loaderImage:{
    width: 300,
    height: 300,
    alignSelf: 'center'
  },
  slider: { 
    width: '50%',
    marginHorizontal:85,
    marginVertical: 30, 
    height: 20, 
    transform: [{scale: 2}]
  },
  logoutIcon: {
    height: 30,
    width: 30,
    marginHorizontal: 5,
  }
});



const styles_ios= StyleSheet.create({
  page: {
    backgroundColor: '#111111',
    flex: 1,
    padding: 10,
  },
  input_header: {
    fontFamily: 'Source Sans Pro',
    fontSize: 25,
    fontWeight: '700',
    marginTop: 20,
    marginBottom:10,
    marginHorizontal:10,
    color: '#E9A9CC'
  },
  imageContainer: {
    flexDirection: 'row',
    gap: 20,
    marginTop: 10,
    marginBottom: 20,
  },
  buttonContainer: {
    alignItems: 'center',
    marginHorizontal: 5
  },
  touchableSize: {
    backgroundColor: '#E9FDFF',
    paddingVertical:5,
    width: 100,
    borderRadius: 32,
  },
  activeSize: {
    backgroundColor: '#8121D7',
  },
  image: {
    width: 25,
    height: 25,
  },
  imageActive: {
    width: 25,
    height: 25,
  },
  buttonText: {
    color: '#111111',
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
    textAlign:'center',
    fontSize: 16,
  },
  buttonTextActive:{
    color: '#E9FDFF'
  },
  buttonTextRest: {
    marginTop: 5,
    marginHorizontal:10,
    color: '#E9A9CC',
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
    fontSize: 18,
  },
  buttonTextStyle: {
    marginTop: 5,
    color: '#1C4042',
    fontFamily: 'Source Sans Pro',
    fontSize: 12,
    textAlign: 'center',
    fontWeight: '700',
  },
  buttonTextStyleActive: {
    marginTop: 5,
    color: '#E9FDFF',
    fontFamily: 'Source Sans Pro',
    fontSize: 12,
    textAlign: 'center',
    fontWeight: '700',
  },
  touchableStyle: {
    backgroundColor: '#E9FDFF',
    width: 70,
    height: 25,
    borderRadius: 20,
  },
  activeStyle: {
    backgroundColor: '#1C4042',
    borderRadius: 20,
  },
  socialsContainer:{
    flexDirection: 'row',
    gap:20,
    marginHorizontal:5,
    marginBottom: 10
  },
  touchableSocial: {
    borderWidth: 0
  },
  activeSocial:{
    borderWidth: 3,
    borderColor: '#8121D7',
    borderRadius: 16
  },
  generate_button: {
    marginLeft: 8,
    marginRight:30,
    marginTop: 20,
    marginBottom: 20,
    padding: 10,
    backgroundColor: '#8121D7',
    borderRadius: 30,
  },
  generate_buttonText: {
    color: 'white',
    fontSize: 18,
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
    textAlign: 'center',
  },
  popupContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#111111',
  },
  loadingText: {
    color: '#E9FDFF',
    marginTop: 10,
    fontSize: 18,
    textAlign: 'center',
    fontFamily: 'Source Sans Pro',
    fontWeight: '700',
  },
  loaderContainer: {
    transform: [{scale: 0.35}]
  },
  loaderImage:{
    width: 300,
    height: 300,
    alignSelf: 'center'
  },
  slider: { 
    width: '50%',
    marginHorizontal:5,
    marginVertical: 30, 
    height: 20, 
    transform: [{scale: 2}]
  },
  logoutIcon: {
    height: 30,
    width: 30,
    marginHorizontal: 5,
  }
});