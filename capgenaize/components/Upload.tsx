import React, { useState, useRef, useEffect, useLayoutEffect } from 'react';
import {
  Alert,
  AlertButton,
  Platform,
  View,
  Image,
  TextInput,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  ScrollView,
  LogBox,
  Modal
} from 'react-native';
import { useNavigation,useRoute } from '@react-navigation/native';
import DocumentPicker, { DocumentPickerResponse } from 'react-native-document-picker';
import Video from 'react-native-video';
import { GooglePlacesAutocomplete } from 'react-native-google-places-autocomplete';
import axios from 'axios'; 
import {NativeStackScreenProps} from "@react-navigation/native-stack"
import {RootStackParamList} from '../App';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface Address {
  city: string;
  country: string;
}

function parseAddress(input: string): Address | null {
  const regex = /([^,]+),[^,]+,([^,]+)/;
  const match = input.match(regex);
  
  if (match) {
    const city = match[1].trim();
    const country = match[2].trim();
    return { city, country };
  }
  
  return null; // return null if the input format doesn't match
}

type UploadProps = NativeStackScreenProps<RootStackParamList, 'Upload'>
const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;


export default function Upload({navigation}: UploadProps) {

  useEffect(() => {
    LogBox.ignoreAllLogs(true);
  }, []);
  

  const [imageUri, setImageUri] = useState('');
  const [selectedFile, setSelectedFile] = useState<DocumentPickerResponse | null>();
  const [memory, setMemory] = useState<string>('');
  const searchInput = useRef(null);
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const [extension, setExtension] = useState('');
  const browse = async () => {
    try {
      const doc: DocumentPickerResponse[] | DocumentPickerResponse | null = await DocumentPicker.pickSingle({
        type: [DocumentPicker.types.images, DocumentPicker.types.video],
      });
      setImageUri(doc.uri)

      if (doc) {
        const allowedExtensions = ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'qt'];
        const fileName = doc.name || ''; // Ensure fileName is not null
        const fileExtension = fileName.split('.').pop()?.toLowerCase() || '';
        
        if (allowedExtensions.includes(fileExtension)) {
          setImageUri(doc.uri);
          setSelectedFile(doc);
          if(fileExtension === 'jpg' || fileExtension === 'jpeg' || fileExtension === 'png')
            setExtension('image');
          else
            setExtension('video');
        } else {
          console.log('Invalid file type. Only jpg, png, jpeg images, mp4, quicktime, and mov videos are allowed.');
        }
      }
    } catch (error) {
      if (DocumentPicker.isCancel(error)) {
        // User canceled the picker
        console.log('User canceled the picker');
      } else {
        // Error occurred while picking the document
        console.log('Error occurred while picking the document:', error);
      }
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
  };

  const handlePress = async()=>{
    setLoading(true);
    const token = await AsyncStorage.getItem("token");
    if (selectedFile) {
      try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        if(address){
          const location = parseAddress(address);
          formData.append('address', JSON.stringify(location));
        }
        axios
      .post(
        "http://192.168.0.159:9000/upload_file",formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": 'multipart/form-data',
          },
          withCredentials: true,
        }
      )
      .then((res) => {
        const file = res.data.file_name;
        console.log(selectedFile.name);
          navigation.push('Generate', {
            memory: memory,
            address: address,
            filename: file,
            filenameURI: imageUri
          });
          setLoading(false);
      })
      .catch((err) => {
        console.log("Error", err);
      });
      } catch (error) {
        console.log('Error occurred while sending the file:', error);
      }
    } else {
      console.log('No file selected');
    }
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
      title: 'Upload Files',
    });
  }, [navigation]);
  return (
    <View style={(Platform.OS == 'android')?styles_android.container:styles_ios.container}>
      <View >
        <ScrollView contentContainerStyle={(Platform.OS == 'android')?styles_android.pageContainer:styles_ios.pageContainer} keyboardShouldPersistTaps="handled">
          <View style={(Platform.OS == 'android')?styles_android.page:styles_ios.page}>
            <Text style={(Platform.OS == 'android')?styles_android.input_header:styles_ios.input_header}>Throwback</Text>
            <TextInput
              style={(Platform.OS == 'android')?styles_android.input: styles_ios.input}
              placeholder="Tell us something about this pic/video (Optional)"
              placeholderTextColor="#E9A9CC"
              value={memory}
              onChangeText={(text) => {
                setMemory(text);
              }}
            />
            <Text style={(Platform.OS == 'android')?styles_android.input_header_location: styles_ios.input_header_location}>Location</Text>
            {/* <ScrollView horizontal={true} style={{width: "95%" }}> */}
            <GooglePlacesAutocomplete
              styles={{
                textInputContainer: {
                  backgroundColor: '#111111',
                  paddingHorizontal: 5,
                  borderBottomWidth: 3,
                  borderBottomColor: '#8121D7'
                },
                textInput: {
                  height: 38,
                  color: '#E9FDFF',
                  backgroundColor:'transparent',
                  fontSize: 16,
                  marginVertical: 5
                },
                predefinedPlacesDescription: {
                  color: '#E9FDFF',
                },
                row:{
                  backgroundColor: '#2D2D2D',
                  color: '#E9FDFF'
                },
                description:{
                  color: "#E9FDFF"
                }
              }}
              placeholder="Search Location"
              textInputProps={{
                placeholderTextColor: '#E9A9CC'
              }}
              onPress={(data, details = null) => {
                setAddress('');
                setAddress(data.description)
              }}
              query={{
                key: 'REACT_APP_MAP_API',
                language: 'en',
              }}
              enablePoweredByContainer={false}
            />
            {/* </ScrollView> */}
            
            <TouchableOpacity style={(Platform.OS == 'android')?styles_android.file_upload_box: styles_ios.file_upload_box} onPress={browse}>
              {selectedFile && selectedFile.type && selectedFile.type.includes('image') ? (
                <Image style={(Platform.OS == 'android')?styles_android.file_preview_image: styles_ios.file_preview_image} source={{ uri: selectedFile.uri }} resizeMode="contain" />
              ) : selectedFile && selectedFile.type && selectedFile.type.includes('video') ? (
                <Video style={(Platform.OS == 'android')?styles_android.file_preview_video: styles_ios.file_preview_video} source={{ uri: selectedFile.uri }} paused={true} resizeMode="cover" />
              ) : (
                <React.Fragment>
                  <Image style={(Platform.OS == 'android')?styles_android.file_upload_image: styles_ios.file_upload_image} source={require('../assets/add.png')} />
                  <Text style={(Platform.OS == 'android')?styles_android.file_upload_text:styles_ios.file_upload_text}>Tap here to upload files from the system:</Text>
                </React.Fragment>
              )}
              {selectedFile && (
                <TouchableOpacity style={(Platform.OS == 'android')?styles_android.remove_button: styles_ios.remove_button} onPress={removeFile}>
                  <Image style={(Platform.OS == 'android')?styles_android.remove_button_icon: styles_ios.remove_button_icon} source={require('../assets/remove.png')} />
                </TouchableOpacity>
              )}
            </TouchableOpacity>
            <TouchableOpacity style={(Platform.OS == 'android')?styles_android.next_button: styles_ios.next_button} onPress={handlePress}>
              <Text style={(Platform.OS == 'android')?styles_android.next_buttonText: styles_ios.next_buttonText}>Next</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
      <Modal visible={loading} transparent>
        <View style={(Platform.OS == 'android')?styles_android.popupContainer: styles_ios.popupContainer}>
          <Image source={require('../assets/upload_file_loading.png')} style={(Platform.OS == 'android')?styles_android.loaderImage: styles_ios.loaderImage}/>
          <Image source={require('../assets/loader.gif') } style={(Platform.OS == 'android')?styles_android.loaderContainer: styles_ios.loaderContainer}/>
          <Text style={(Platform.OS == 'android')?styles_android.loadingText: styles_ios.loadingText}>Uploading the file...</Text>
        </View>
      </Modal>
    </View>
  );
}

const styles_android = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#111111',
  },
  pageContainer: {
    flexGrow: 1,
    paddingBottom: 20,
  },
  page: {
    borderTopStartRadius: 30,
    borderTopEndRadius: 30,
    paddingVertical: 5,
    paddingHorizontal: 15,
    marginHorizontal: 10
  },
  input_header: {
    fontFamily: 'Source Sans Pro',
    color: '#E9A9CC',
    fontWeight: '700',
    marginTop: 20,
    marginBottom: 10,

    fontSize: 20,
  },
  input_header_location: {
    fontFamily: 'Source Sans Pro',
    color: '#E9A9CC',
    fontWeight: '700',
    marginTop: 0,
    marginBottom: 10,
    fontSize: 20,
  },
  input: {
    backgroundColor: 'transparent',
    marginBottom: 20,
    paddingHorizontal: 8,
    borderBottomWidth: 3,
    borderBottomColor: '#8121D7',
    color: '#E9FDFF',
  },
  file_upload_box: {
    backgroundColor: '#2D2D2D',
    height: 350,
    borderRadius: 20,
    borderWidth: 3,
    marginVertical: 20,  
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
    marginHorizontal: -5
  },
  file_upload_text: {
    fontFamily: 'Source Sans Pro',
    fontSize: 18,
    color: '#E9A9CC'
  },
  file_upload_image: {
    height: 50,
    width: 50,
  },
  file_preview_image: {
    flex: 1,
    width: windowWidth - 70,
    borderRadius: 32,
  },
  file_preview_video: {
    flex: 1,
    borderRadius: 32,
  },
  remove_button: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    borderRadius: 10,
    padding: 5,
  },
  remove_button_icon: {
    width: 15,
    height: 15,
    tintColor: '#E9FDFF',
  },
  next_button: {
    marginTop: 10,
    marginBottom: 20,
    padding: 10,
    backgroundColor: '#8121D7',
    borderRadius: 30,
  },
  next_buttonText: {
    color: '#E9FDFF',
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
    marginHorizontal: 5,
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
  logoutIcon: {
    height: 30,
    width: 30,
    marginHorizontal: 5,
  }
});


const styles_ios = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#111111',
  },
  pageContainer: {
    flexGrow: 1,
    paddingBottom: 20,
  },
  page: {
    borderTopStartRadius: 30,
    borderTopEndRadius: 30,
    paddingVertical: 5,
    paddingHorizontal: 15,
    marginHorizontal: 10
  },
  input_header: {
    fontFamily: 'Source Sans Pro',
    color: '#E9A9CC',
    fontWeight: '700',
    marginTop: 20,
    marginBottom: 10,

    fontSize: 20,
  },
  input_header_location: {
    fontFamily: 'Source Sans Pro',
    color: '#E9A9CC',
    fontWeight: '700',
    marginTop: 0,
    marginBottom: 10,
    fontSize: 20,
  },
  input: {
    backgroundColor: 'transparent',
    marginBottom: 20,
    paddingHorizontal: 8,
    borderBottomWidth: 3,
    borderBottomColor: '#8121D7',
    color: '#E9FDFF',
  },
  file_upload_box: {
    backgroundColor: '#2D2D2D',
    height: 350,
    borderRadius: 20,
    borderWidth: 3,
    marginVertical: 20,  
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
    marginHorizontal: -5
  },
  file_upload_text: {
    fontFamily: 'Source Sans Pro',
    fontSize: 18,
    color: '#E9A9CC'
  },
  file_upload_image: {
    height: 50,
    width: 50,
  },
  file_preview_image: {
    flex: 1,
    width: windowWidth - 70,
    borderRadius: 32,
  },
  file_preview_video: {
    flex: 1,
    width: windowWidth - 70,
    borderRadius: 32,
  },
  remove_button: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    borderRadius: 10,
    padding: 5,
  },
  remove_button_icon: {
    width: 15,
    height: 15,
    tintColor: '#E9FDFF',
  },
  next_button: {
    marginTop: 10,
    marginBottom: 20,
    padding: 10,
    backgroundColor: '#8121D7',
    borderRadius: 30,
  },
  next_buttonText: {
    color: '#E9FDFF',
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
    marginHorizontal: 5,
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
  logoutIcon: {
    height: 30,
    width: 30,
    marginHorizontal: 5,
  }
});
