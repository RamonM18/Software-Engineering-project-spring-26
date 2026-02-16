import java.io.IOException;
import java.net.*;
import java.nio.ByteBuffer;

public class UDPConnection {

    private DatagramSocket senderSocket;
    private DatagramSocket receiverSocket;
    private InetAddress targetAddress;

    public UDPConnection() {
        try {
            this.targetAddress = InetAddress.getByName("127.0.0.1");
            this.senderSocket = new DatagramSocket(null);
            this.receiverSocket = new DatagramSocket(null);
            this.senderSocket.setReuseAddress(true);
            this.receiverSocket.setReuseAddress(true);
            this.senderSocket = new DatagramSocket(7500);
            this.receiverSocket = new DatagramSocket(7501);
            this.receiverSocket.setSoTimeout(10);
        } catch (SocketException | UnknownHostException e) {
            System.err.println("Initialization failed: " + e.getMessage());
        }
    }

    public void sendTo(int value) {
        try {
            byte[] data = ByteBuffer.allocate(4).putInt(value).array(); //Length 4 bc 4 digit socket address
            DatagramPacket packet = new DatagramPacket(data, data.length, targetAddress, 7501);
            senderSocket.send(packet);
        } catch (IOException e) {
            System.err.println("Send error: " + e.getMessage());
        }
    }

    public Integer recvfrom() {
        byte[] buffer = new byte[4];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

        try {
            receiverSocket.receive(packet); // Will only wait for 10ms
            return ByteBuffer.wrap(packet.getData()).getInt();
        } catch (SocketTimeoutException e) {
            // No data was waiting; this is normal in a non-threaded loop
            return null; 
        } catch (IOException e) {
            System.err.println("Receive error: " + e.getMessage());
            return null;
        }
    }

    public void setNetworkAddress(String ipAddress) {
        try {
            this.targetAddress = InetAddress.getByName(ipAddress);
        } catch (UnknownHostException e) {
            System.err.println("Invalid IP.");
        }
    }
    
    // Test Main
    public static void main(String[] args) {
        UDPConnection comms = new UDPConnection();
        
        // Simulating a game loop
        for (int i = 0; i < 5; i++) {
            comms.sendTo(100 + i);
            
            // Manually check for data
            Integer input = comms.recvfrom();
            if (input != null) {
                System.out.println("Player equipment code: " + input);
            }
        }
    }
}