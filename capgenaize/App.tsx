import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { DocumentPickerResponse } from 'react-native-document-picker';
import Home from './components/Home';
import Register from './components/Sign Up-Sign In/Register';
import Login from './components/Sign Up-Sign In/Login';
import Forgot from './components/Sign Up-Sign In/Forgot';
import Upload from './components/Upload';
import Generate from './components/Generate';
import Caption from './components/Caption';

export type RootStackParamList = {
  Home: undefined;
  Generate: {
    memory: string;
    address: string;
    filename: DocumentPickerResponse | null;
    filenameURI: string;
  };
  Register: undefined;
  Login: undefined;
  Forgot: undefined;
  Upload: undefined;
  Caption: { caption: string; filename: string; file_path: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerTitleStyle: {
            fontFamily: 'Josefin Sans',
            color: '#E9FDFF',
            fontWeight: 'bold',
          },
          headerStyle: {
            backgroundColor: '#111111',
          },
          headerTintColor: '#E9FDFF',
        }}
      >
        <Stack.Screen
          name="Home"
          component={Home}
          options={{
            title: '',
          }}
        />
        <Stack.Screen
          name="Register"
          component={Register}
          options={{
            title: 'Sign Up',
          }}
        />
        <Stack.Screen
          name="Login"
          component={Login}
          options={{
            title: 'Sign In',
          }}
        />
        <Stack.Screen
          name="Forgot"
          component={Forgot}
          options={{
            title: 'Reset Password',
          }}
        />
        <Stack.Screen
          name="Upload"
          component={Upload}
          options={{
            title: 'Upload Files',
          }}
        />
        <Stack.Screen
          name="Generate"
          component={Generate}
          options={{
            title: 'Choose Caption',
          }}
        />
        <Stack.Screen
          name="Caption"
          component={Caption}
          options={{
            title: 'Caption',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}