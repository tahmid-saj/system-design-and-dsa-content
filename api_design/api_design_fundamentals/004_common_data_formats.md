# Common data formats

## Textual data formats

We can serialize data using serialization methods provided by a language, such as Marshal in Ruby, pickle in Python, Serializable in Java, and so on. External libraries can also be used for this purpose, but they have some common problems. They are language-specific and can tight-couple APIs to that language. Furthermore, these methods lack efficient version control mechanisms and are generally inefficient regarding CPU utilization and encoded data size. Therefore, developers prefer using standardized encoding formats—such as XML, JSON, Protobuf, Avro, and so on—instead of built-in encoding methods.

JSON, XML, and CSV are data representation formats that use Unicode characters (text) and support encoding in many languages. The most popular way clients interact with web APIs is by serializing data into XML and JSON formats. CSV is less powerful than XML and JSON because it doesn’t support the data hierarchy and is commonly used when dealing with data in tabular form. These structures have a standardized encoding style, and clients can easily extract and consume data by deserializing it into their respective languages. Text-based representation formats have the following common characteristics:

- Schemaless structure: Data-related information (metadata) is embedded within the format structure.

- Machine-readable: The data is well structured and can be easily interpreted by machines.

- Human-readable: Data is represented in Unicode characters that humans can read and understand.

- Object representation: Data can embed programming objects in a defined format.

In the following sections, we’ll discuss XML and JSON, two well-known text data formats for developing APIs.

### XML

Extensible Markup Language (XML) is a restricted form/subset of Standard Generalized Markup Language (SGML) and is designed for storing and exchanging data on the web. XML has a syntax similar to HTML documents. It uses tags to construct objects, but unlike HTML, tags are not predefined. This means that users can create custom tags to define elements. Generally, tags are used as keys to identify data elements and can also have attributes defining metadata that can help data filtering and sorting, etc. An element's value is stored within an object's opening and closing tags. The illustrations below describe the structure of an XML message, along with an example.

<img width="718" alt="image" src="https://github.com/user-attachments/assets/e987649f-f2e6-4d00-b1f4-76a28b633b2d">

The tag <?xml ?> in the XML document above defines the XML version and encoding style used in the document and is part of the processing instructions for applications. XML follows a tree-based structure and the message tag represents the root element of the document. This is contrast to the head and body tags, which are children of the root element message, and author and text are children of body.

#### XML advantages

XML provides a robust and extensible structural representation by using namespaces to define and reuse data-related information in a standardized way. It supports features like XPath and XQuery. It also supports adding new entities over time without affecting the functionality of existing ones. XML is highly portable and is being used in a variety of different domains, described below:

Note: Namespaces are a way to resolve naming conflicts in XML. It allows developers to create collections of names (with the goal of standardizing them across different implementations) and associate them with URIs for global identification on the Internet. 

Note: XPath is a method for selecting nodes or entities in an XML document.

Note: XQuery is a functional programming language for querying and transforming XML data.

- XML is widely used in electronic data interchange to quickly and securely access information between different systems. For example, SOAP uses XML for secure (encapsulates sensitive content in an XML envelope) business-to-business data exchange, while WordPress supports XML-RPC to communicate with other systems.

- XML offers streamlined methods for accessing information (XPath, XQuery, etc.), and its search results are precise. Because of this simplicity and efficiency in obtaining information, XML is popular in the web automation industry for building crawlers and web bots.

- XML supports the storage and exchange of complex data in a standardized way. For example, it’s used in the wireless communication industry, such as VoiceWeb, Personal Digital Assistants, and so on.

#### XML disadvantages

While XML is widespread and has many benefits, it also has some disadvantages when it comes to choosing a data format in API design:

- Repeated declaration of tags makes it verbose and redundant.

- It has a large file size due to the amount of tags maintaining the document structure.

- XML lacks a built-in mechanism for distinguishing numbers from their string representation.

- Lack of support for binary strings (raw bytes of data without character encoding).

- Although XML supports optional schema definitions, applications tend to hard-code their logic for interpreting data.

### JSON

JavaScript Object Notation (JSON) is a subset of the JavaScript language and is famous for its built-in browser support. It efficiently handles client-side and server-side scripts with the added benefit of simplicity and readability. It uses colon-separated key-value pairs to describe data attributes. JSON supports four primitive data types: strings, numbers, booleans, and null. The data is structured using the following six characters:

- Left curly bracket ({): Marks the start of a data object

- Right curly bracket (}): Marks the end of a data object

- Left square bracket ([): Indicates the start of an array

- Right square bracket (]): Indicates the end of an array

- Colon (:): Separates the key/name from the value

- Comma (,): Separate key-value pairs from each other

Here is the JSON representation of the same message object that was discussed in the earlier section on XML format:

<img width="386" alt="image" src="https://github.com/user-attachments/assets/eefbc0a7-5945-4baf-8cba-63756135b9bb">

#### JSON advantages

The goal of JSON is to be structurally minimal while being a portable and flexible subset of JavaScript. It has the following advantages over textual data format competitors:

- Language-independent and has a lower learning curve than XML.

- Gaining more and more attention with the increasing popularity of Node.js and JavaScript in web and mobile applications.

- Lightweight and parses faster than XML.

- More compact and has lower network latency than XML.

#### JSON disadvantages

JSON is still on its way to maturity in comparison to XML, and the following issues have yet to be addressed:

- Lacks a standardized way to define and reuse common descriptions for JSON documents.

- Lacks a built-in way to distinguish between numbers and floats in a JSON document.

- Does not support precision beyond 253 for a 64-bit numeric representation and can cause parsing errors.

- Despite JSON supporting schema definition, the use of schema is not as widespread, and hard-coded interpretation logic for data such as numbers and binary strings can cause compatibility issues.

Note: We can use a Base64 encoding to send raw bytes without giving the data any character representation. But it might not be the most optimally compact representation.

Let's see how these data formats map to our general criteria of optimal data format:

<img width="623" alt="image" src="https://github.com/user-attachments/assets/f33785f1-bc99-4ffc-9052-718b93249e83">

Why is JSON so popular in web applications?

JSON is designed to represent the data structures present in most programming languages ​​in a simpler way without having to learn the tree-based data binding provided by formats like XML. The semantics of JSON for representing data structures are similar to those of programming languages, which makes it easier to learn and interpret data objects from JSON. Additionally, JavaScript is the most commonly used language in web applications, further driving the adaptation of JSON in the web industry.

When should we prefer XML over JSON?

Both XML and JSON have similar properties. However, XML may be preferable to JSON when the data contains complex structures, such as those found in books, articles, and other datasets. XML can represent documents containing various data structures because it represents data in a tree-like format, making it easier to manage different data structures in an organized manner. It also supports custom attributes and provides methods such as XPath and XQuery, which are suitable for large metadata sets representing complex structures.

## Binary data formats

Text-based data representation is often preferred when interacting with different clients, especially when client implementations are outside of an organization’s control. This is because it’s easier to analyze and debug when the data is human-readable. For internal use, such as in iOS and Android applications (where the organization controls both ends of the communication tightly), there’s more freedom and flexibility in choosing the data format, and we can move to formats that are more compact, faster to parse, and lighter on the database. The binary encoding formats share the following benefits in common:

- Machine-friendly: The data is in binary format and can be processed with little or no preprocessing.

- Schema dependent: Data-related information is defined in the schema document. A schema document contains templates on how to structure data into a specific format.

- Portability: Binary formats can be easily deserialized into different languages ​​as long as they have the same encoding and decoding schema.

- Precision support: Binary format can store large numbers (variable length integers) and floating point numbers with greater precision.

- Standardized: The binary format uses a well-defined schema that's well-documented and can be standardized across different implementations.

Many binary formats exist, such as MessagePack, Fast Infoset, BSON, WBXML, Protobuf, Thrift, Avro, and so on. Let's see how the message object above looks when encoded in MessagePack, a binary variant of JSON:

<img width="708" alt="image" src="https://github.com/user-attachments/assets/e9e1e253-d5ba-485a-bb88-2fcee1465680">

The binary version of the above message object is demonstrated in the image below:

<img width="611" alt="image" src="https://github.com/user-attachments/assets/404e8dc3-8f8c-4e53-8674-586d1410353c">

MessagePack and other binary variants of JSON and XML follow a schemaless encoding style that increases the size of the encoded data and are not common in API development. For example, in the above illustration, disablelinks takes an extra 12 bytes to encode the field name, whereas its value is only one byte, representing true.

### Thrift and Protobuf

The most commonly used binary data formats are Protocol buffers (Protobuf) and Apache Thrift. Google developed Protocol Buffers, and Facebook developed Apache Thrift. Both these binary encoding libraries follow similar rules and have been open-sourced for standardized public use. They have a similar-looking schema, shown below:

<img width="715" alt="image" src="https://github.com/user-attachments/assets/fdf5f26e-1105-4669-a2f0-162b301fdb6a">

We can breakdown these schema definitions as follows:

- Tags: Each field is identified by the numbers equivalent to the names. For example, 1 identifies the fields nodeID for Thrift and node_id for Protobuf. These tags are encoded in data rather than field names, allowing for more compact data representation.

- Labels: The markers required, optional, and repeated (Protobuf only) imply checks to determine whether to raise an error when encoding or decoding data. These markers are only added to the schema but are not encoded in the transmitted data.

- Types: Each field can define its data type (string, i64, int64, etc.) by specifying a type marker. Protobuf does not have a type to represent arrays, and it uses the repeated label to show that the data can have multiple occurrences.

- Names: The markers (nodeID, node_id, etc.) represent the names of the data entity. One thing worth noting here is that these are not identifiers for fields, which allow the name to be changed without affecting the implementation.

Note: The use of the label, repeated, in Protobuf allows flexibility to change a single variable to an array of variables in different schema versions, but it’s only valid for optional fields, otherwise it can cause compatibility problems. To read more, see Thrift documentation and Protobuf documentation.

### Apache Avro

Apache Avro is also an open-source binary encoding format developed by Hadoop. Avro supports two schema styles, Avro IDL and JSON-based definitions. JSON is well-known in the industry and allows developers to create schemas without having to learn another language. Avro doesn’t add tags and types like Thrift and Protobuf and uses a value-only data encoding style. It relies on the schema version defined in the data reader to identify the fields when decoded. If there are any conflicts due to different versions of the writer's and reader's schema, the Avro library resolves these conflicts through a side-by-side comparison of these versions, as shown below.

Note: A data reader is a program that translates raw data into useful information or object representations by using a well-defined schema.

<img width="611" alt="image" src="https://github.com/user-attachments/assets/99bcbb9c-ee80-44c5-bccf-f11c9c5bb2c4">

Here, the field name is used as the field's identifier, so the records can be in any order as long as the field name remains the same. If the reader code finds a field that is not in the reader schema, it just ignores that field. On the other hand, if the record doesn’t contain the fields expected by the reader schema, the reader code populates it with the default values ​​specified in the reader schema.

Avro is very flexible with dynamically generated schemas. It handles schema transitions efficiently when decoding, and administrators don’t have to worry about manually updating field names, tags, types, and so on, in order to make them compatible with new versions. Thrift and Protobuf, on the other hand, generate dynamic code and perform compile-time checks (type safety, and so forth) for different statically typed languages ​​such as C, C++, Java, C#, and more. Avro also supports dynamic code generation as optimization over statically typed languages. However, dynamic code generation is not required, especially when dealing with dynamically typed languages.

## Binary format advantages and disadvantages

Binary formats are much more compact and faster in terms of processing than text-based formats. They’re flexible with clearly defined version compatibility and dynamically-generated code support. However, when it comes to human interaction, they require preprocessing to make them human-readable. Let’s see how these binary formats map to our general criteria of an optimal data format, outlined in the table below:

<img width="659" alt="image" src="https://github.com/user-attachments/assets/972345c6-ce00-4c62-87df-4a3231209046">

## Data format summary

Choosing a data exchange format for an API is always debatable, because each format is suitable for some use cases and may have drawbacks for others. However, this section provides general recommendations for using the textual and binary data formats discussed in this chapter.

- JSON is probably the ideal choice when dealing with small groups of systems, especially those developed in JavaScript, where human-readability is essential.

- XML is probably the ideal format of choice when dealing with various systems with complex data structures that require markup and human-readability.

- Avro is likely the ideal choice when dealing with large files, frequent interactions of data encoded using different schema versions, and significant encoding sizes.

- Protobuf or Thrift may serve the purpose when network latency, interprocess communication, and processing speed are paramount.

The choice is not limited to the data formats discussed above; other formats, such as YAML, FormData, SQL, and so on, can also be considered. We can also introduce a custom format when an existing format doesn't meet our needs, keeping in mind the cost and effort required for internal or external usage. In other words, usage within the system or when sending information to end users.

Why is binary data small in size and high performing compared to textual ones?

Binary representation uses compression algorithms like LZ77, RLE, etc., to reduce file sizes. Although, the real gain is not only through compression, but also through reducing markup (extra information required for data serialization and deserialization). Most binary formats define schemas for serializing/deserializing data, which are either transmitted once or saved in the database to reduce the size of each request. The smaller size makes the binary data optimized for storing and sending data over the wire. Moreover, binary data doesn’t need to be converted to another format for processing (since the CPU also performs computations in binary). Therefore, binary data is the most compact and high-performing format.




