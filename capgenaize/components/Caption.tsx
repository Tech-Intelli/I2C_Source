import React, {useLayoutEffect} from 'react';
import { Alert,AlertButton, Platform, View, Text, TouchableOpacity, StyleSheet, Image, ScrollView } from 'react-native';
import Typing from './Text Streaming/Typing';
import { RootStackParamList } from '../App';
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import Clipboard from '@react-native-clipboard/clipboard';
import Video from 'react-native-video';
import axios from 'axios';
type CaptionProps = NativeStackScreenProps<RootStackParamList, 'Caption'>

export default function Caption({ route, navigation }: CaptionProps) {
  const { caption, filename, file_path } = route.params;
  const handleRegenerate = () => {
    navigation.goBack();
  }

  const handleReUpload = () => {
    navigation.goBack();
    navigation.goBack();
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

  const handleCopy = () => {
    Clipboard.setString(caption);
    showAlert("Caption copied successfully!");
  };
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
      title: 'Caption',
    });
  }, [navigation]);
  return (
    <View style={(Platform.OS == 'android') ? styles_android.page_container : styles_ios.page_container}>
      <ScrollView>
        <View style={(Platform.OS == 'android') ? styles_android.preview_card : styles_ios.preview_card}>
          <View style={(Platform.OS == 'android') ? styles_android.image_container : styles_ios.image_container}>
            {filename.includes('image') ? (
              <Image source={{ uri: file_path }} style={(Platform.OS == 'android') ? styles_android.image : styles_ios.image} />
            ) : (
                <Video source={{ uri: filename }} style={(Platform.OS == 'android') ? styles_android.video : styles_ios.video} />
              )}
          </View>
          <View style={(Platform.OS == 'android') ? styles_android.caption_card : styles_ios.caption_card}>
            <Text style={(Platform.OS == 'android') ? styles_android.caption_text : styles_ios.caption_text}>
              <Typing text={[caption]} />
            </Text>
          </View>
        </View>
        <TouchableOpacity style={(Platform.OS == 'android') ? styles_android.share_button : styles_ios.share_button} onPress={handleCopy}>
          <Text style={(Platform.OS == 'android') ? styles_android.share_text : styles_ios.share_text}>Copy</Text>
          <Image style={(Platform.OS == 'android') ? styles_android.button_image : styles_ios.button_image} source={require('../assets/copy.png')} />
        </TouchableOpacity>
        <TouchableOpacity style={(Platform.OS == 'android') ? styles_android.share_button : styles_ios.share_button} onPress={handleReUpload}>
          <Text style={(Platform.OS == 'android') ? styles_android.share_text : styles_ios.share_text}>Reupload</Text>
          <Image style={(Platform.OS == 'android') ? styles_android.button_image : styles_ios.button_image} source={require('../assets/reupload.png')} />
        </TouchableOpacity>
        <TouchableOpacity style={(Platform.OS == 'android') ? styles_android.share_button : styles_ios.share_button} onPress={handleRegenerate}>
          <Text style={(Platform.OS == 'android') ? styles_android.share_text : styles_ios.share_text}>Regenerate</Text>
          <Image style={(Platform.OS == 'android') ? styles_android.button_image : styles_ios.button_image} source={require('../assets/regenerate.png')} />
        </TouchableOpacity>
      </ScrollView>
    </View>
  )
}

const styles_android = StyleSheet.create({
    page_container:{
        backgroundColor: '#111111',
        flex:1,
        padding: 32
    },
    caption_card:{
        marginTop: 5,
    },
    caption_text: {
        fontSize: 15,
        fontFamily: 'Source Sans Pro',
        color: '#E9FDFF'
    },
    preview_card:{
        backgroundColor: '#2D2D2D',
        padding:32,
        borderRadius:32,
        margin: 10
    },
    preview_card_username:{
        flexDirection: 'row',
        gap: 5
    },
    image:{
        width:250,
        height:150,
        borderRadius:16,
        justifyContent:'center'
    },
    image_container:{
        flexDirection: 'row',
        justifyContent:'center'
    },
    functions:{
        flexDirection: 'row',
        justifyContent: 'space-between'
    },
    functions_1:{
        flexDirection:'row',
        gap: 3
    },
    add_buttons:{
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginHorizontal: 20
    },
    add:{
        backgroundColor: '#8121D7',
        width: 140,
        borderRadius: 32,
        marginVertical: 10,
        paddingVertical: 5,
        flexDirection: 'row',
        gap: 5,
        justifyContent: 'center'
    },
    add_text:{
        color: '#E9FDFF',
        fontSize: 18,
        marginVertical: 3,
        marginHorizontal: 5,
        textAlign: 'center'
    },
    share_button:{
        backgroundColor:'#8121D7',
        marginHorizontal: 20,
        marginVertical: 10,
        paddingVertical: 10,
        borderRadius:32,
        flexDirection: 'row',
        gap: 10,
        justifyContent: 'center'
    },
    share_text: {
        fontSize:18,
        color: "#E9FDFF",
        textAlign: 'center'
    },
    button_image:{
        height: 24,
        width: 24
    },
    video:{
        width:250,
        height:150,
        borderRadius:16,
        justifyContent:'center'
    },
    logoutIcon: {
      height: 30,
      width: 30,
      marginHorizontal: 5,
    }

});

const styles_ios = StyleSheet.create({
    page_container:{
        backgroundColor: '#111111',
        flex:1,
        padding: 32
    },
    caption_card:{
        marginTop: 5,
    },
    caption_text: {
        fontSize: 15,
        fontFamily: 'Source Sans Pro',
        color: '#E9FDFF'
    },
    preview_card:{
        backgroundColor: '#2D2D2D',
        padding:32,
        borderRadius:32,
        margin: 10
    },
    preview_card_username:{
        flexDirection: 'row',
        gap: 5
    },
    image:{
        width:250,
        height:150,
        borderRadius:16,
        justifyContent:'center'
    },
    image_container:{
        flexDirection: 'row',
        justifyContent:'center'
    },
    functions:{
        flexDirection: 'row',
        justifyContent: 'space-between'
    },
    functions_1:{
        flexDirection:'row',
        gap: 3
    },
    add_buttons:{
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginHorizontal: 20
    },
    add:{
        backgroundColor: '#8121D7',
        width: 140,
        borderRadius: 32,
        marginVertical: 10,
        paddingVertical: 5,
        flexDirection: 'row',
        gap: 5,
        justifyContent: 'center'
    },
    add_text:{
        color: '#E9FDFF',
        fontSize: 18,
        marginVertical: 3,
        marginHorizontal: 5,
        textAlign: 'center'
    },
    share_button:{
        backgroundColor:'#8121D7',
        marginHorizontal: 20,
        marginVertical: 10,
        paddingVertical: 10,
        borderRadius:32,
        flexDirection: 'row',
        gap: 10,
        justifyContent: 'center'
    },
    share_text: {
        fontSize:18,
        color: "#E9FDFF",
        textAlign: 'center'
    },
    button_image:{
        height: 24,
        width: 24
    },
    video:{
        width:250,
        height:150,
        borderRadius:16,
        justifyContent:'center'
    },
    logoutIcon: {
      height: 30,
      width: 30,
      marginHorizontal: 5,
    }

});