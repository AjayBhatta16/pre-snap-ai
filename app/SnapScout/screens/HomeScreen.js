import styles from "../assets/styles"
import { View, Text, Image, Button } from "react-native"

export default HomeScreen = ({ navigation }) => {
    const handleScan = () => {
        // insert camera stuff here
        navigation.navigate('form')
    }

    return (
        <View style={styles.container}>
            <Image source={require('../assets/favicon.png')} />
            <Text style={styles.title}>SnapScout AI</Text>
            <Text style={styles.description}>Welcome to SnapScout, your friendly neighborhood football play predictor! Scan a play to get started.</Text>
            <Button 
                title="Scan A Play" 
                onPress={handleScan}
            />
        </View>
    )
}