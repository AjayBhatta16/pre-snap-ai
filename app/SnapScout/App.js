import HomeScreen  from './screens/HomeScreen'
import FormScreen from './screens/FormScreen'
import PredictionScreen from './screens/PredictionScreen'
import { useState } from 'react';

export default function App() {
  const [screen, setScreen] = useState('home');

  const navigate = (target) => {
    setScreen(target);
  };

  if (screen == 'home') {
    return <HomeScreen navigation={{navigate}} />
  } else if (screen == 'form') {
    return <FormScreen navigation={{navigate}} />
  } else if (screen == 'prediction') {
    return <PredictionScreen navigation={{navigate}} />
  }
}
