import javalang
import re
from tqdm import tqdm
from multiprocessing import Pool,cpu_count
import random
from urllib.parse import urlparse


def mask_identifiers(java_code): #takes a string of java code and returns masked code and mapping

    # Parse the Java code
    tokens = list(javalang.tokenizer.tokenize(java_code))
    parser = javalang.parser.Parser(tokens)
    tree = parser.parse()

    # Reserved Java keywords
    reserved_keywords = {
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 
    'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 
    'int', 'interface', 'long', 'native', 'new', 'null', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 
    'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 
    'Override', 'Deprecated', 'SuppressWarnings', 'SafeVarargs', 'FunctionalInterface', 'Retention', 'Documented', 'Target', 
    'Inherited', 'Repeatable', 'Native', 'Generated', 'PostConstruct', 'PreDestroy', 'Resource', 'Resources', 'Transitional', 
    'XmlAccessorOrder', 'XmlAccessorType', 'XmlAnyElement', 'XmlAnyAttribute', 'XmlAttribute', 'XmlElement', 'XmlElementDecl', 
    'XmlElementRef', 'XmlElementRefs', 'XmlElements', 'XmlEnum', 'XmlEnumValue', 'XmlID', 'XmlIDREF', 'XmlInlineBinaryData', 
    'XmlJavaTypeAdapter', 'XmlList', 'XmlMimeType', 'XmlNs', 'XmlNsForm', 'XmlRootElement', 'XmlSchema', 'XmlSchemaType', 
    'XmlSchemaTypes', 'XmlSeeAlso', 'XmlTransient', 'XmlType', 'XmlValue'
}

    
    standard_libraries = {
    'System', 'String', 'Integer', 'Double', 'Math', 'List', 'ArrayList', 'LinkedList', 'HashMap', 'HashSet', 'Hashtable', 
    'TreeMap', 'TreeSet', 'Queue', 'Deque', 'PriorityQueue', 'Stack', 'Vector', 'Scanner', 'File', 'FileReader', 'FileWriter', 
    'BufferedReader', 'PrintWriter', 'InputStream', 'OutputStream', 'DataInputStream', 'DataOutputStream', 'ObjectInputStream', 
    'ObjectOutputStream', 'PrintStream', 'InputStreamReader', 'OutputStreamWriter', 'URLConnection', 'URL', 'URI', 'Date', 
    'Calendar', 'TimeZone', 'Locale', 'BigDecimal', 'BigInteger', 'Random', 'UUID', 'Collections', 'Arrays', 'EnumSet', 
    'EnumMap', 'Stream', 'Optional', 'Comparator', 'Iterable', 'Iterator', 'Spliterator', 'Collector', 'Collectors', 'Path', 
    'Paths', 'Files', 'FileSystems', 'FileVisitor', 'FileFilter', 'FileNameFilter', 'Charset', 'StandardCharsets', 'Pattern', 
    'Matcher', 'DateFormat', 'SimpleDateFormat', 'NumberFormat', 'DecimalFormat', 'MessageFormat', 'Format', 'Scanner', 
    'Locale', 'TimeZone', 'Currency', 'Observer', 'Observable', 'Timer', 'TimerTask', 'Thread', 'Runnable', 'ThreadLocal', 
    'Callable', 'Executor', 'ExecutorService', 'ScheduledExecutorService', 'CompletionService', 'Future', 'FutureTask', 
    'Semaphore', 'CountDownLatch', 'CyclicBarrier', 'Lock', 'ReadWriteLock', 'Condition', 'AtomicInteger', 'AtomicLong', 
    'AtomicReference', 'AtomicBoolean', 'Math', 'StrictMath', 'System', 'Runtime', 'Process', 'ProcessBuilder', 'ClassLoader', 
    'SecurityManager', 'ThreadGroup', 'Package', 'Compiler', 'Math', 'StrictMath'
}

    standard_methods = {
    'out', 'err', 'println', 'print', 'printf', 'format', 'scanf', 'next', 'nextLine', 'nextInt', 'nextDouble', 'hasNext', 
    'hasNextLine', 'hasNextInt', 'hasNextDouble', 'close', 'flush', 'read', 'write', 'append', 'toString', 'valueOf', 'equals', 
    'hashCode', 'getClass', 'wait', 'notify', 'notifyAll', 'run', 'start', 'sleep', 'join', 'yield', 'interrupt', 'isAlive', 
    'isDaemon', 'setPriority', 'getPriority', 'setDaemon', 'getState', 'getThreadGroup', 'currentThread', 'yield', 'sleep', 
    'setSecurityManager', 'getSecurityManager', 'availableProcessors', 'freeMemory', 'totalMemory', 'gc', 'exit', 'load', 
    'loadLibrary', 'mapLibraryName', 'getStackTrace', 'getThreadInfo', 'getThreadMXBean', 'getThreadGroup', 'getLockInfo', 
    'getMonitorInfo', 'findMonitorDeadlockedThreads', 'findDeadlockedThreads', 'halt', 'exec', 'load', 'runFinalizersOnExit', 
    'traceMethodCalls', 'runFinalization', 'exit', 'arraycopy', 'identityHashCode', 'getDeclaredMethod', 'getMethod', 
    'getMethods', 'getDeclaredMethods', 'getConstructor', 'getConstructors', 'forName', 'newInstance', 'isInstance', 
    'isAssignableFrom', 'asSubclass', 'getModifiers', 'getDeclaredFields', 'getFields', 'getDeclaredField', 'getField', 
    'getEnumConstants', 'getDeclaredClasses', 'getClasses', 'isAnnotation', 'isSynthetic', 'isInterface', 'isPrimitive', 
    'getPackage', 'getPackages', 'getDeclaredPackage', 'getPackageAnnotations', 'getAnnotations', 'getDeclaredAnnotations', 
    'getAnnotation', 'isAnnotationPresent', 'getClassLoader', 'getProtectionDomain', 'getGenericSuperclass', 
    'getGenericInterfaces', 'getComponentType', 'getGenericComponentType', 'getDeclaringClass', 'getEnclosingClass', 
    'getEnclosingConstructor', 'getEnclosingMethod', 'getEnclosingElement', 'isEnum', 'isAnonymousClass', 'isLocalClass', 
    'isMemberClass', 'getTypeName', 'getModifiers', 'getDeclaredConstructors', 'getConstructors', 'getDeclaredMethods', 
    'getMethods', 'getField', 'getDeclaredFields', 'getFields', 'getDeclaredField', 'getMethod', 'getDeclaredMethod', 
    'asSubclass', 'cast', 'newProxyInstance'
}
    # Collect all user-defined identifiers (variables, class names, method names)
    variables = set()
    classes = set()
    methods = set()

    for path, node in tree.filter(javalang.tree.VariableDeclarator):
        variables.add(node.name)

    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        classes.add(node.name)

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        if node.name not in reserved_keywords:
            methods.add(node.name)

    # Collect imported libraries and their packages
    imported_libraries = set()
    imported_classes = set()
    package_names = set()
    for path, node in tree.filter(javalang.tree.Import):
        parts = node.path.split('.')
        package_names.update(parts[:-1])
        imported_classes.add(parts[-1])

    # Create a mapping from identifiers to their masked versions
    variable_mapping = {name: f"[U_VARIABLE]{name}" for name in variables}
    class_mapping = {name: f"[U_CLASS]{name}" for name in classes}
    method_mapping = {name: f"[U_METHOD]{name}" for name in methods}

    # Combine all user-defined mappings into one
    identifier_mapping = {**variable_mapping, **class_mapping, **method_mapping}

    # Mark reserved keywords and standard library identifiers
    reserved_mapping = {keyword: f"[R]{keyword}" for keyword in reserved_keywords}
    library_mapping = {lib: f"[S_CLASS]{lib}" for lib in standard_libraries | imported_classes}
    package_mapping = {pkg: f"[S_PACKAGE]{pkg}" for pkg in package_names}
    method_mapping_std = {method: f"[S_METHOD]{method}" for method in standard_methods}

    # Combine all mappings
    complete_mapping = {**identifier_mapping, **reserved_mapping, **library_mapping, **package_mapping, **method_mapping_std}

    # Function to replace identifiers with their masked versions
    def replace_identifiers(match):
        identifier_name = match.group(0)
        return complete_mapping.get(identifier_name, identifier_name)

    # Mask method calls explicitly without redundant replacement
    def mask_method_calls(java_code):
        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if node.member in standard_methods or node.qualifier in imported_classes or node.qualifier in standard_libraries:
                pattern = re.compile(r'\b' + re.escape(node.member) + r'\b')
                if not pattern.search(f"[S_METHOD]{node.member}"):
                    java_code = pattern.sub(f"[S_METHOD]{node.member}", java_code)
        return java_code

    # Use regular expressions to replace all identifiers in the code
    masked_code = re.sub(r'\b(?:' + '|'.join(re.escape(id) for id in complete_mapping) + r')\b', replace_identifiers, java_code)
    
    # Mask method calls
    masked_code = mask_method_calls(masked_code)

    return masked_code, complete_mapping

def process_line(line):
    line = line.rstrip()
    line = "public class my_wrapper {" + line + "}"
    masked_code, complete_mapping = mask_identifiers(line)
    start_index = len("[R]public [R]class [U_CLASS]my_wrapper {")
    end_index = len(masked_code) - len("}")
    clean_masked_code = masked_code[start_index:end_index]
    if(clean_masked_code==masked_code):
        print()
        print("matched")
        print()
    return clean_masked_code

def processed_write(input_file,output_file): # takes input file of java code in every line and output file and writes processed masked code to output file
    with open(input_file, "r") as file1:
        java_code = file1.readlines()

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_line, java_code), total=len(java_code)))

    with open(output_file, "w") as file2:
        for masked_code in results:
            file2.write(masked_code)
            file2.write("\n")


def string_cut(line): # Cut the line at a random position
    remain_ratio=random.uniform(.5,.7)
    words=line.count(" ")
    words_to_remain=int(words*remain_ratio)+1
    cut_space_pos=0
    for letter in line:
        cut_space_pos+=1
        if letter==" ":
            words_to_remain-=1
            if words_to_remain==0:
                break
    return line[:cut_space_pos]



def fit_in_shape(code: str, comment: str,tokenizer, code_length=382, comment_length=126): # Fit code and comment into the specified shape
    max_length=code_length+comment_length
    # Tokenize the code and comment
    tokenized_code = tokenizer.tokenize(code)
    tokenized_comment = tokenizer.tokenize(comment)

    # Check the lengths
    len_code = len(tokenized_code)
    len_comment = len(tokenized_comment)

    # Case 1: If the sum of lengths is less than or equal to max_length
    if len_code + len_comment <= max_length:
        return tokenizer.convert_tokens_to_string(tokenized_code) , tokenizer.convert_tokens_to_string( tokenized_comment)

    # Case 2: If code length > code_length and comment length <= comment_length
    elif len_code > code_length and len_comment <= comment_length:
        return tokenizer.convert_tokens_to_string(tokenized_code[:max_length - len_comment]) ,  tokenizer.convert_tokens_to_string(tokenized_comment)

    # Case 3: If code length <= code_length and comment length > comment_length
    elif len_code <= code_length and len_comment > comment_length:
        return tokenizer.convert_tokens_to_string(tokenized_code) ,  tokenizer.convert_tokens_to_string(tokenized_comment[:max_length - len_code])

    # Case 4: If code length > code_length and comment length > comment_length
    elif len_code > code_length and len_comment > comment_length:
        return tokenizer.convert_tokens_to_string(tokenized_code[:code_length]) ,  tokenizer.convert_tokens_to_string(tokenized_comment[:comment_length])

    else:
        return "Invalid lengths for code and comment."
    


 
def remove_url(text, replacement_text=""): # Remove URLs from text
    words = text.split()
    for i, word in enumerate(words):
        parsed_url = urlparse(word)
        if parsed_url.scheme and parsed_url.netloc:
            words[i] = replacement_text
    return ' '.join(words)


def truncate_string(text, max_length, tokenizer): # Truncate text to max_length tokens
    tokenized_text = tokenizer.tokenize(text)
    if len(tokenized_text) <= max_length:
        return tokenizer.convert_tokens_to_string(tokenized_text)
    else:
        return tokenizer.convert_tokens_to_string(tokenized_text[:max_length])
    
def create_batches(sentences, batch_size):
    for i in range(0, len(sentences), batch_size):
        yield sentences[i:i + batch_size]



def sort_and_reorder(tokenizer, list1, list_of_lists): # Sort and reorder the list of sentences based on the length of tokenized sentences
    
    # Zip together index and length of each tokenized sentence
    indexed_lengths = [(i, len(tokenizer.encode(lines))) for i, lines in enumerate(list1)]
    
    # Sort the zip based on the length of tokenized sentences
    indexed_lengths.sort(key=lambda x: x[1])
    
    # Extract the sorted indices
    sorted_indices = [i for i, _ in indexed_lengths]
    
    # Reorder list1 based on the sorted indices
    sorted_list1 = [list1[i] for i in sorted_indices]
    
    # Reorder each list in list_of_lists based on the sorted indices
    sorted_list_of_lists = [[lst[i] for i in sorted_indices] for lst in list_of_lists]
    
    return sorted_list1, sorted_list_of_lists


