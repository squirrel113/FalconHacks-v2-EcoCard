import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import Homepage from "./routes/home/Homepage";

export default function App() {
  return (
    <NavigationContainer>
      <Homepage />
    </NavigationContainer>
  );
}
