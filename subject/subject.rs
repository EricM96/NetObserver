use std::net::TcpStream;
use std::string::String;
use std::str;
use std::io::{BufRead, BufReader, Write};

fn main() {

    // set up socket
    let mut stream = TcpStream::connect("127.0.0.1:8080").expect("Failed to connect to server"); // socket 
    let mut buffer: Vec<u8> = Vec::new(); // buffer (for replies) 
    let msg = String::from("Hello there!\n"); // message to send
    let mut msg_bytes = msg.as_bytes();

    stream.write(&mut msg_bytes).expect("Failed to write to socket"); //send msg

    let mut reader = BufReader::new(&stream); // reader to put reply into buffer
    reader.read_until(b'\n', &mut buffer).expect("Failed to read into buffer");
    print!("{}", str::from_utf8(&buffer).expect("Failed to output buffer"));

}