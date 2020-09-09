---
title: "빔 단어세기 예제"
aliases: /use/wordcount-example/
---
<!--
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# 아파치 빔 단어세기 예제

{{< toc >}}

{{< language-switcher java py go >}}

단어세기 예제는 텍스트를 읽고, 텍스트의 각 줄을 토큰화 하여 개별 단어로 만들고, 생성된 단어들에 대해 빈도 계산을 수행하는 분산 처리 파이프라인을 설정하는 방법을 보여줍니다. 빔 개발 도구에는 이러한 단어세기 예제가 네개 포함되어 있으며 이 예제들은 간단한 예제부터 점점 확장되어 자세해지고 복잡해집니다. 모든 예제의 입력 텍스트는 셰익스피어의 작품을 사용하겠습니다.

각 단어세기 예제는 빔 프로그래밍 모델의 여러 다른 개념들을 소개합니다. 가장 간단한 예제인 MinimalWordCount를 이해하는 것부터 시작합니다. 파이프라인 작성의 기본원리에 익숙해지고 나면 좀 더 복잡한 예제를 통해 추가적인 개념들을 배우게 될 것입니다.

* **MinimalWordCount**는 파이프라인 작성의 기본 원리에 대해 보여줍니다.
* **WordCount**는 재사용가능하고 쉽게 유지보수 할 수 있는 파이프라인을 작성하는 모범 사례를 소개합니다. 
* **DebuggingWordCount**는 로그를 남기고 파이프라인을 디버깅 하는 방법을 소개합니다.
* **WindowedWordCount**는 빔의 프로그래밍 모델을 사용하여 어떻게 유한하고 무한한 데이터셋 모두를 다루는지에 대해 보여줍니다.

## MinimalWordCount 예제

MinimalWordCount는 DirectRunner를 이용하여 텍스트 파일을 읽고 토큰화 하고 단어 수를 세어 출력 텍스트 파일에 기록하는 간단한 파이프라인을 실행하는 방법을 보여줍니다.

{{< paragraph class="language-java language-go" >}}
이 예제는 입력과 출력 파일이 소스코드에 고정되어 있으며 오류가 있는지 따로 확인하지 않습니다. 가장 단순하게 빔 파이프라인을 만드는 법을 보여드리는 것이 목적이기 때문입니다. 이 파이프라인은 매개변수화 되지 않았기 때문에 일반적으로 사용되는 빔 파이프라인보다 다양한 실행기와의 호환성이 부족합니다. 이후 이어질 예제에서 파이프라인의 입출력 소스들을 매개변수화 하고 다른 올바른 사용방법들도 보여드릴 것입니다.
{{< /paragraph >}}

{{< highlight java >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.MinimalWordCount
{{< /highlight >}}

{{< highlight py >}}
python -m apache_beam.examples.wordcount_minimal --input YOUR_INPUT_FILE --output counts
{{< /highlight >}}

{{< highlight go >}}
$ go install github.com/apache/beam/sdks/go/examples/minimal_wordcount
$ minimal_wordcount
{{< /highlight >}}

{{< paragraph class="language-java" >}}
자바로 짜여진 전체 코드를 보고 싶다면 다음을 보세요:
**[MinimalWordCount](https://github.com/apache/beam/blob/master/examples/java/src/main/java/org/apache/beam/examples/MinimalWordCount.java).**
{{< /paragraph >}}

{{< paragraph class="language-py" >}}
파이썬으로 짜여진 전체 코드를 보고 싶다면 다음을 보세요:
**[wordcount_minimal.py](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount_minimal.py).**
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
고로 짜여진 전체 코드를 보고 싶다면 다음을 보세요:
**[minimal_wordcount.go](https://github.com/apache/beam/blob/master/sdks/go/examples/minimal_wordcount/minimal_wordcount.go).**
{{< /paragraph >}}

**핵심 개념들:**

* 파이프라인 생성하기
* 파이프라인에 변환기 적용하기
* 입력 읽기 (이 예제의 경우 텍스트 파일들을 읽기)
* ParDo 변환기 적용하기
* 개발 도구에서 제공하는 변환기 적용하기 (이 예제의 경우 Count)
* 출력 쓰기 (이 예제의 경우 텍스트 파일에 쓰기)
* 파이프라인 실행하기

이어지는 섹션에서는 MinimalWordCount 파이프라인의 코드를 짚어가며 이러한 개념들을 자세히 설명합니다.

### Creating the pipeline

{{< paragraph class="language-java language-py" >}}
In this example, the code first creates a `PipelineOptions` object. This object
lets us set various options for our pipeline, such as the pipeline runner that
will execute our pipeline and any runner-specific configuration required by the
chosen runner. In this example we set these options programmatically, but more
often, command-line arguments are used to set `PipelineOptions`.
{{< /paragraph >}}

{{< paragraph class="language-java language-py" >}}
You can specify a runner for executing your pipeline, such as the
`DataflowRunner` or `SparkRunner`. If you omit specifying a runner, as in this
example, your pipeline executes locally using the `DirectRunner`. In the next
sections, we will specify the pipeline's runner.
{{< /paragraph >}}

{{< highlight java >}}
 // Create a PipelineOptions object. This object lets us set various execution
 // options for our pipeline, such as the runner you wish to use. This example
 // will run with the DirectRunner by default, based on the class path configured
 // in its dependencies.
 PipelineOptions options = PipelineOptionsFactory.create();
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_options >}}
{{< /highlight >}}

{{< paragraph class="language-java language-py" >}}
The next step is to create a `Pipeline` object with the options we've just
constructed. The Pipeline object builds up the graph of transformations to be
executed, associated with that particular pipeline.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
The first step is to create a `Pipeline` object. It builds up the graph of
transformations to be executed, associated with that particular pipeline.
The scope allows grouping into composite transforms.
{{< /paragraph >}}

{{< highlight java >}}
Pipeline p = Pipeline.create(options);
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_create >}}
{{< /highlight >}}

{{< highlight go >}}
p := beam.NewPipeline
s := p.Root()
{{< /highlight >}}

### Applying pipeline transforms

The MinimalWordCount pipeline contains several transforms to read data into the
pipeline, manipulate or otherwise transform the data, and write out the results.
Transforms can consist of an individual operation, or can contain multiple
nested transforms (which is a [composite transform](/documentation/programming-guide#composite-transforms)).

Each transform takes some kind of input data and produces some output data. The
input and output data is often represented by the SDK class `PCollection`.
`PCollection` is a special class, provided by the Beam SDK, that you can use to
represent a dataset of virtually any size, including unbounded datasets.

<img src="/images/wordcount-pipeline.svg" width="800px" alt="The MinimalWordCount pipeline data flow.">

*Figure 1: The MinimalWordCount pipeline data flow.*

The MinimalWordCount pipeline contains five transforms:

1.  A text file `Read` transform is applied to the `Pipeline` object itself, and
    produces a `PCollection` as output. Each element in the output `PCollection`
    represents one line of text from the input file. This example uses input
    data stored in a publicly accessible Google Cloud Storage bucket ("gs://").

{{< highlight java >}}
p.apply(TextIO.read().from("gs://apache-beam-samples/shakespeare/*"))
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_read >}}
{{< /highlight >}}

{{< highlight go >}}
lines := textio.Read(s, "gs://apache-beam-samples/shakespeare/*")
{{< /highlight >}}

2.  This transform splits the lines in `PCollection<String>`, where each element
    is an individual word in Shakespeare's collected texts.
    As an alternative, it would have been possible to use a
    [ParDo](/documentation/programming-guide/#pardo)
    transform that invokes a `DoFn` (defined in-line as an anonymous class) on
    each element that tokenizes the text lines into individual words. The input
    for this transform is the `PCollection` of text lines generated by the
    previous `TextIO.Read` transform. The `ParDo` transform outputs a new
    `PCollection`, where each element represents an individual word in the text.

{{< highlight java >}}
    .apply("ExtractWords", FlatMapElements
        .into(TypeDescriptors.strings())
        .via((String line) -> Arrays.asList(line.split("[^\\p{L}]+"))))
{{< /highlight >}}

{{< highlight py >}}
# The Flatmap transform is a simplified version of ParDo.
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_pardo >}}
{{< /highlight >}}

{{< highlight go >}}
words := beam.ParDo(s, func(line string, emit func(string)) {
    for _, word := range wordRE.FindAllString(line, -1) {
        emit(word)
    }
}, lines)
{{< /highlight >}}

3.  The SDK-provided `Count` transform is a generic transform that takes a
    `PCollection` of any type, and returns a `PCollection` of key/value pairs.
    Each key represents a unique element from the input collection, and each
    value represents the number of times that key appeared in the input
    collection.

    In this pipeline, the input for `Count` is the `PCollection` of individual
    words generated by the previous `ParDo`, and the output is a `PCollection`
    of key/value pairs where each key represents a unique word in the text and
    the associated value is the occurrence count for each.

{{< highlight java >}}
.apply(Count.<String>perElement())
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_count >}}
{{< /highlight >}}

{{< highlight go >}}
counted := stats.Count(s, words)
{{< /highlight >}}

4.  The next transform formats each of the key/value pairs of unique words and
    occurrence counts into a printable string suitable for writing to an output
    file.

    The map transform is a higher-level composite transform that encapsulates a
    simple `ParDo`. For each element in the input `PCollection`, the map
    transform applies a function that produces exactly one output element.

{{< highlight java >}}
.apply("FormatResults", MapElements
    .into(TypeDescriptors.strings())
    .via((KV<String, Long> wordCount) -> wordCount.getKey() + ": " + wordCount.getValue()))
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_map >}}
{{< /highlight >}}

{{< highlight go >}}
formatted := beam.ParDo(s, func(w string, c int) string {
    return fmt.Sprintf("%s: %v", w, c)
}, counted)
{{< /highlight >}}

5.  A text file write transform. This transform takes the final `PCollection` of
    formatted Strings as input and writes each element to an output text file.
    Each element in the input `PCollection` represents one line of text in the
    resulting output file.

{{< highlight java >}}
.apply(TextIO.write().to("wordcounts"));
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_write >}}
{{< /highlight >}}

{{< highlight go >}}
textio.Write(s, "wordcounts.txt", formatted)
{{< /highlight >}}

{{< paragraph class="language-java language-py" >}}
Note that the `Write` transform produces a trivial result value of type `PDone`,
which in this case is ignored.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
Note that the `Write` transform returns no PCollections.
{{< /paragraph >}}

### Running the pipeline

{{< paragraph class="language-java language-py" >}}
Run the pipeline by calling the `run` method, which sends your pipeline to be
executed by the pipeline runner that you specified in your `PipelineOptions`.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
Run the pipeline by passing it to a runner.
{{< /paragraph >}}

{{< highlight java >}}
p.run().waitUntilFinish();
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_minimal_run >}}
{{< /highlight >}}

{{< highlight go >}}
direct.Execute(context.Background(), p)
{{< /highlight >}}

{{< paragraph class="language-java language-py" >}}
Note that the `run` method is asynchronous. For a blocking execution, call the
<span class="language-java">`waitUntilFinish`</span>
<span class="language-py">`wait_until_finish`</span> method on the result object
returned by the call to `run`.
{{< /paragraph >}}

## WordCount example

This WordCount example introduces a few recommended programming practices that
can make your pipeline easier to read, write, and maintain. While not explicitly
required, they can make your pipeline's execution more flexible, aid in testing
your pipeline, and help make your pipeline's code reusable.

This section assumes that you have a good understanding of the basic concepts in
building a pipeline. If you feel that you aren't at that point yet, read the
above section, [MinimalWordCount](#minimalwordcount-example).

**To run this example in Java:**

{{< highlight class="runner-direct" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--inputFile=pom.xml --output=counts" -Pdirect-runner
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--runner=FlinkRunner --inputFile=pom.xml --output=counts" -Pflink-runner
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
$ mvn package exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--runner=FlinkRunner --flinkMaster=<flink master> --filesToStage=target/word-count-beam-bundled-0.1.jar \
                  --inputFile=/path/to/quickstart/pom.xml --output=/tmp/counts" -Pflink-runner

You can monitor the running job by visiting the Flink dashboard at http://<flink master>:8081
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--runner=SparkRunner --inputFile=pom.xml --output=counts" -Pspark-runner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--runner=DataflowRunner --gcpTempLocation=gs://YOUR_GCS_BUCKET/tmp \
                  --project=YOUR_PROJECT --region=GCE_REGION \
                  --inputFile=gs://apache-beam-samples/shakespeare/* --output=gs://YOUR_GCS_BUCKET/counts" \
     -Pdataflow-runner
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--inputFile=pom.xml --output=counts --runner=SamzaRunner" -Psamza-runner
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
$ mvn package -Pnemo-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WordCount \
     --runner=NemoRunner --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
$ mvn package -P jet-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WordCount \
     --runner=JetRunner --jetLocalMode=3 --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

To view the full code in Java, see
**[WordCount](https://github.com/apache/beam/blob/master/examples/java/src/main/java/org/apache/beam/examples/WordCount.java).**

**To run this example in Python:**

{{< highlight class="runner-direct" >}}
python -m apache_beam.examples.wordcount --input YOUR_INPUT_FILE --output counts
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
python -m apache_beam.examples.wordcount --input /path/to/inputfile \
                                         --output /path/to/write/counts \
                                         --runner FlinkRunner
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
# Running Beam Python on a distributed Flink cluster requires additional configuration.
# See https://beam.apache.org/documentation/runners/flink/ for more information.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
python -m apache_beam.examples.wordcount --input /path/to/inputfile \
                                         --output /path/to/write/counts \
                                         --runner SparkRunner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
# As part of the initial setup, install Google Cloud Platform specific extra components.
pip install apache-beam[gcp]
python -m apache_beam.examples.wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
                                         --output gs://YOUR_GCS_BUCKET/counts \
                                         --runner DataflowRunner \
                                         --project YOUR_GCP_PROJECT \
                                         --region YOUR_GCP_REGION \
                                         --temp_location gs://YOUR_GCS_BUCKET/tmp/
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

To view the full code in Python, see
**[wordcount.py](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount.py).**

**To run this example in Go:**

{{< highlight class="runner-direct" >}}
$ go install github.com/apache/beam/sdks/go/examples/wordcount
$ wordcount --input <PATH_TO_INPUT_FILE> --output counts
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ go install github.com/apache/beam/sdks/go/examples/wordcount
# As part of the initial setup, for non linux users - install package unix before run
$ go get -u golang.org/x/sys/unix
$ wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
            --output gs://<your-gcs-bucket>/counts \
            --runner dataflow \
            --project your-gcp-project \
            --region your-gcp-region \
            --temp_location gs://<your-gcs-bucket>/tmp/ \
            --staging_location gs://<your-gcs-bucket>/binaries/ \
            --worker_harness_container_image=apache/beam_go_sdk:latest
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

To view the full code in Go, see
**[wordcount.go](https://github.com/apache/beam/blob/master/sdks/go/examples/wordcount/wordcount.go).**

**New Concepts:**

* Applying `ParDo` with an explicit `DoFn`
* Creating Composite Transforms
* Using Parameterizable `PipelineOptions`

The following sections explain these key concepts in detail, and break down the
pipeline code into smaller sections.

### Specifying explicit DoFns

{{< paragraph class="language-java language-py" >}}
When using `ParDo` transforms, you need to specify the processing operation that
gets applied to each element in the input `PCollection`. This processing
operation is a subclass of the SDK class `DoFn`. You can create the `DoFn`
subclasses for each `ParDo` inline, as an anonymous inner class instance, as is
done in the previous example (MinimalWordCount). However, it's often a good
idea to define the `DoFn` at the global level, which makes it easier to unit
test and can make the `ParDo` code more readable.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
When using `ParDo` transforms, you need to specify the processing operation that
gets applied to each element in the input `PCollection`. This processing
operation is either a named function or a struct with specially-named methods. You
can use anomynous functions (but not closures). However, it's often a good
idea to define the `DoFn` at the global level, which makes it easier to unit
test and can make the `ParDo` code more readable.
{{< /paragraph >}}

{{< highlight java >}}
// In this example, ExtractWordsFn is a DoFn that is defined as a static class:

static class ExtractWordsFn extends DoFn<String, String> {
    ...

    @ProcessElement
    public void processElement(ProcessContext c) {
        ...
    }
}
{{< /highlight >}}

{{< highlight py >}}
# In this example, the DoFns are defined as classes:

{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_wordcount_dofn >}}
{{< /highlight >}}

{{< highlight go >}}
// In this example, extractFn is a DoFn that is defined as a function:

func extractFn(ctx context.Context, line string, emit func(string)) {
   ...
}
{{< /highlight >}}

### Creating composite transforms

{{< paragraph class="language-java language-py" >}}
If you have a processing operation that consists of multiple transforms or
`ParDo` steps, you can create it as a subclass of `PTransform`. Creating a
`PTransform` subclass allows you to encapsulate complex transforms, can make
your pipeline's structure more clear and modular, and makes unit testing easier.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
If you have a processing operation that consists of multiple transforms or
`ParDo` steps, you can use a normal Go function to encapsulate them. You can
furthermore use a named subscope to group them as a composite transform visible
for monitoring.
{{< /paragraph >}}

{{< paragraph class="language-java language-py" >}}
In this example, two transforms are encapsulated as the `PTransform` subclass
`CountWords`. `CountWords` contains the `ParDo` that runs `ExtractWordsFn` and
the SDK-provided `Count` transform.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
In this example, two transforms are encapsulated as a `CountWords` function.
{{< /paragraph >}}

When `CountWords` is defined, we specify its ultimate input and output; the
input is the `PCollection<String>` for the extraction operation, and the output
is the `PCollection<KV<String, Long>>` produced by the count operation.

{{< highlight java >}}
public static class CountWords extends PTransform<PCollection<String>,
    PCollection<KV<String, Long>>> {
  @Override
  public PCollection<KV<String, Long>> expand(PCollection<String> lines) {

    // Convert lines of text into individual words.
    PCollection<String> words = lines.apply(
        ParDo.of(new ExtractWordsFn()));

    // Count the number of times each word occurs.
    PCollection<KV<String, Long>> wordCounts =
        words.apply(Count.<String>perElement());

    return wordCounts;
  }
}

public static void main(String[] args) throws IOException {
  Pipeline p = ...

  p.apply(...)
   .apply(new CountWords())
   ...
}
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_wordcount_composite >}}
{{< /highlight >}}

{{< highlight go >}}
func CountWords(s beam.Scope, lines beam.PCollection) beam.PCollection {
	s = s.Scope("CountWords")

	// Convert lines of text into individual words.
	col := beam.ParDo(s, extractFn, lines)

	// Count the number of times each word occurs.
	return stats.Count(s, col)
}
{{< /highlight >}}

### Using parameterizable PipelineOptions

You can hard-code various execution options when you run your pipeline. However,
the more common way is to define your own configuration options via command-line
argument parsing. Defining your configuration options via the command-line makes
the code more easily portable across different runners.

{{< paragraph class="language-java language-py" >}}
Add arguments to be processed by the command-line parser, and specify default
values for them. You can then access the options values in your pipeline code.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
You can use the standard `flag` package for this purpose.
{{< /paragraph >}}

{{< highlight java >}}
public static interface WordCountOptions extends PipelineOptions {
  @Description("Path of the file to read from")
  @Default.String("gs://dataflow-samples/shakespeare/kinglear.txt")
  String getInputFile();
  void setInputFile(String value);
  ...
}

public static void main(String[] args) {
  WordCountOptions options = PipelineOptionsFactory.fromArgs(args).withValidation()
      .as(WordCountOptions.class);
  Pipeline p = Pipeline.create(options);
  ...
}
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" examples_wordcount_wordcount_options >}}
{{< /highlight >}}

{{< highlight go >}}
var input = flag.String("input", "gs://apache-beam-samples/shakespeare/kinglear.txt", "File(s) to read.")

func main() {
    ...
    p := beam.NewPipeline()
    s := p.Root()

    lines := textio.Read(s, *input)
    ...
{{< /highlight >}}

## DebuggingWordCount example

The DebuggingWordCount example demonstrates some best practices for
instrumenting your pipeline code.

**To run this example in Java:**

{{< highlight class="runner-direct" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.DebuggingWordCount \
     -Dexec.args="--output=counts" -Pdirect-runner
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.DebuggingWordCount \
     -Dexec.args="--runner=FlinkRunner --output=counts" -Pflink-runner
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
$ mvn package exec:java -Dexec.mainClass=org.apache.beam.examples.DebuggingWordCount \
     -Dexec.args="--runner=FlinkRunner --flinkMaster=<flink master> --filesToStage=target/word-count-beam-bundled-0.1.jar \
                  --output=/tmp/counts" -Pflink-runner

You can monitor the running job by visiting the Flink dashboard at http://<flink master>:8081
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.DebuggingWordCount \
     -Dexec.args="--runner=SparkRunner --output=counts" -Pspark-runner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.DebuggingWordCount \
   -Dexec.args="--runner=DataflowRunner --gcpTempLocation=gs://<your-gcs-bucket>/tmp \
                --project=YOUR_PROJECT --region=GCE_REGION \
                --inputFile=gs://apache-beam-samples/shakespeare/* --output=gs://<your-gcs-bucket>/counts" \
     -Pdataflow-runner
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.DebuggingWordCount \
     -Dexec.args="--runner=SamzaRunner --output=counts" -Psamza-runner
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
$ mvn package -Pnemo-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.DebuggingWordCount \
     --runner=NemoRunner --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
$ mvn package -P jet-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.DebuggingWordCount \
     --runner=JetRunner --jetLocalMode=3 --output=counts
{{< /highlight >}}

To view the full code in Java, see
[DebuggingWordCount](https://github.com/apache/beam/blob/master/examples/java/src/main/java/org/apache/beam/examples/DebuggingWordCount.java).

**To run this example in Python:**

{{< highlight class="runner-direct" >}}
python -m apache_beam.examples.wordcount_debugging --input YOUR_INPUT_FILE --output counts
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
# As part of the initial setup, install Google Cloud Platform specific extra components.
pip install apache-beam[gcp]
python -m apache_beam.examples.wordcount_debugging --input gs://dataflow-samples/shakespeare/kinglear.txt \
                                         --output gs://YOUR_GCS_BUCKET/counts \
                                         --runner DataflowRunner \
                                         --project YOUR_GCP_PROJECT \
                                         --temp_location gs://YOUR_GCS_BUCKET/tmp/
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

To view the full code in Python, see
**[wordcount_debugging.py](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount_debugging.py).**

**To run this example in Go:**

{{< highlight class="runner-direct" >}}
$ go install github.com/apache/beam/sdks/go/examples/debugging_wordcount
$ debugging_wordcount --input <PATH_TO_INPUT_FILE> --output counts
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ go install github.com/apache/beam/sdks/go/examples/debugging_wordcount
# As part of the initial setup, for non linux users - install package unix before run
$ go get -u golang.org/x/sys/unix
$ debugging_wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
                      --output gs://<your-gcs-bucket>/counts \
                      --runner dataflow \
                      --project your-gcp-project \
                      --region your-gcp-region \
                      --temp_location gs://<your-gcs-bucket>/tmp/ \
                      --staging_location gs://<your-gcs-bucket>/binaries/ \
                      --worker_harness_container_image=apache-docker-beam-snapshots-docker.bintray.io/beam/go:20180515
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

To view the full code in Go, see
**[debugging_wordcount.go](https://github.com/apache/beam/blob/master/sdks/go/examples/debugging_wordcount/debugging_wordcount.go).**

**New Concepts:**

* Logging
* Testing your Pipeline via `PAssert`

The following sections explain these key concepts in detail, and break down the
pipeline code into smaller sections.

### Logging

Each runner may choose to handle logs in its own way.

{{< highlight java >}}
// This example uses .trace and .debug:

public class DebuggingWordCount {

  public static class FilterTextFn extends DoFn<KV<String, Long>, KV<String, Long>> {
    ...

    @ProcessElement
    public void processElement(ProcessContext c) {
      if (...) {
        ...
        LOG.debug("Matched: " + c.element().getKey());
      } else {
        ...
        LOG.trace("Did not match: " + c.element().getKey());
      }
    }
  }
}
{{< /highlight >}}

{{< highlight py >}}
{{< code_sample "sdks/python/apache_beam/examples/snippets/snippets.py" example_wordcount_debugging_logging >}}
{{< /highlight >}}

{{< highlight go >}}
type filterFn struct {
    ...
}

func (f *filterFn) ProcessElement(ctx context.Context, word string, count int, emit func(string, int)) {
    if f.re.MatchString(word) {
         // Log at the "INFO" level each element that we match.
         log.Infof(ctx, "Matched: %v", word)
         emit(word, count)
    } else {
        // Log at the "DEBUG" level each element that is not matched.
        log.Debugf(ctx, "Did not match: %v", word)
    }
}
{{< /highlight >}}

#### Direct Runner

When executing your pipeline with the `DirectRunner`, you can print log
messages directly to your local console. <span class="language-java">If you use
the Beam SDK for Java, you must add `Slf4j` to your class path.</span>

#### Cloud Dataflow Runner

When executing your pipeline with the `DataflowRunner`, you can use Stackdriver
Logging. Stackdriver Logging aggregates the logs from all of your Cloud Dataflow
job's workers to a single location in the Google Cloud Platform Console. You can
use Stackdriver Logging to search and access the logs from all of the workers
that Cloud Dataflow has spun up to complete your job. Logging statements in your
pipeline's `DoFn` instances will appear in Stackdriver Logging as your pipeline
runs.

{{< paragraph class="language-java language-py" >}}
You can also control the worker log levels. Cloud Dataflow workers that execute
user code are configured to log to Stackdriver Logging by default at "INFO" log
level and higher. You can override log levels for specific logging namespaces by
specifying: `--workerLogLevelOverrides={"Name1":"Level1","Name2":"Level2",...}`.
For example, by specifying `--workerLogLevelOverrides={"org.apache.beam.examples":"DEBUG"}`
when executing a pipeline using the Cloud Dataflow service, Stackdriver Logging
will contain only "DEBUG" or higher level logs for the package in addition to
the default "INFO" or higher level logs.
{{< /paragraph >}}

{{< paragraph class="language-java language-py" >}}
The default Cloud Dataflow worker logging configuration can be overridden by
specifying `--defaultWorkerLogLevel=<one of TRACE, DEBUG, INFO, WARN, ERROR>`.
For example, by specifying `--defaultWorkerLogLevel=DEBUG` when executing a
pipeline with the Cloud Dataflow service, Cloud Logging will contain all "DEBUG"
or higher level logs. Note that changing the default worker log level to TRACE
or DEBUG significantly increases the amount of logs output.
{{< /paragraph >}}

#### Apache Spark Runner

> **Note:** This section is yet to be added. There is an open issue for this
> ([BEAM-792](https://issues.apache.org/jira/browse/BEAM-792)).

#### Apache Flink Runner

> **Note:** This section is yet to be added. There is an open issue for this
> ([BEAM-791](https://issues.apache.org/jira/browse/BEAM-791)).

#### Apache Nemo Runner

When executing your pipeline with the `NemoRunner`, most log messages are printed
directly to your local console. You should add `Slf4j` to your class path to make
full use of the logs. In order to observe the logs on each of the driver and the
executor sides, you should observe the folders created by Apache REEF. For example,
when running your pipeline through the local runtime, a folder called `REEF_LOCAL_RUNTIME`
will be created on your work directory, and the logs and the metric information can
all be found under the directory.

### Testing your pipeline with asserts

{{< paragraph class="language-java language-py" >}}
<span class="language-java">`PAssert`</span><span class="language-py">`assert_that`</span>
is a set of convenient PTransforms in the style of Hamcrest's collection
matchers that can be used when writing pipeline level tests to validate the
contents of PCollections. Asserts are best used in unit tests with small datasets.
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
The `passert` package contains convenient PTransforms that can be used when
writing pipeline level tests to validate the contents of PCollections. Asserts
are best used in unit tests with small datasets.
{{< /paragraph >}}

{{< paragraph class="language-java" >}}
The following example verifies that the set of filtered words matches our
expected counts. The assert does not produce any output, and the pipeline only
succeeds if all of the expectations are met.
{{< /paragraph >}}

{{< paragraph class="language-py language-go" >}}
The following example verifies that two collections contain the same values. The
assert does not produce any output, and the pipeline only succeeds if all of the
expectations are met.
{{< /paragraph >}}

{{< highlight java >}}
public static void main(String[] args) {
  ...
  List<KV<String, Long>> expectedResults = Arrays.asList(
        KV.of("Flourish", 3L),
        KV.of("stomach", 1L));
  PAssert.that(filteredWords).containsInAnyOrder(expectedResults);
  ...
}
{{< /highlight >}}

{{< highlight py >}}
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

with TestPipeline() as p:
  assert_that(p | Create([1, 2, 3]), equal_to([1, 2, 3]))
{{< /highlight >}}

{{< highlight go >}}
...
passert.Equals(s, formatted, "Flourish: 3", "stomach: 1")
{{< /highlight >}}

{{< paragraph class="language-java" >}}
See [DebuggingWordCountTest](https://github.com/apache/beam/blob/master/examples/java/src/test/java/org/apache/beam/examples/DebuggingWordCountTest.java)
for an example unit test.
{{< /paragraph >}}

## WindowedWordCount example

The WindowedWordCount example counts words in text just as the previous
examples did, but introduces several advanced concepts.

**New Concepts:**

* Unbounded and bounded datasets
* Adding timestamps to data
* Windowing
* Reusing PTransforms over windowed PCollections

The following sections explain these key concepts in detail, and break down the
pipeline code into smaller sections.

**To run this example in Java:**

{{< highlight class="runner-direct" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WindowedWordCount \
     -Dexec.args="--inputFile=pom.xml --output=counts" -Pdirect-runner
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WindowedWordCount \
     -Dexec.args="--runner=FlinkRunner --inputFile=pom.xml --output=counts" -Pflink-runner
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
$ mvn package exec:java -Dexec.mainClass=org.apache.beam.examples.WindowedWordCount \
     -Dexec.args="--runner=FlinkRunner --flinkMaster=<flink master> --filesToStage=target/word-count-beam-bundled-0.1.jar \
                  --inputFile=/path/to/quickstart/pom.xml --output=/tmp/counts" -Pflink-runner

You can monitor the running job by visiting the Flink dashboard at http://<flink master>:8081
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WindowedWordCount \
     -Dexec.args="--runner=SparkRunner --inputFile=pom.xml --output=counts" -Pspark-runner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WindowedWordCount \
   -Dexec.args="--runner=DataflowRunner --gcpTempLocation=gs://YOUR_GCS_BUCKET/tmp \
                --project=YOUR_PROJECT --region=GCE_REGION \
                --inputFile=gs://apache-beam-samples/shakespeare/* --output=gs://YOUR_GCS_BUCKET/counts" \
     -Pdataflow-runner
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WindowedWordCount \
     -Dexec.args="--runner=SamzaRunner --inputFile=pom.xml --output=counts" -Psamza-runner
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
$ mvn package -Pnemo-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WindowedWordCount \
     --runner=NemoRunner --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
$ mvn package -P jet-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WindowedWordCount \
     --runner=JetRunner --jetLocalMode=3 --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

To view the full code in Java, see
**[WindowedWordCount](https://github.com/apache/beam/blob/master/examples/java/src/main/java/org/apache/beam/examples/WindowedWordCount.java).**

**To run this example in Python:**

This pipeline writes its results to a BigQuery table `--output_table`
parameter. using the format `PROJECT:DATASET.TABLE` or
`DATASET.TABLE`.

{{< highlight class="runner-direct" >}}
python -m apache_beam.examples.windowed_wordcount --input YOUR_INPUT_FILE --output_table PROJECT:DATASET.TABLE
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
# As part of the initial setup, install Google Cloud Platform specific extra components.
pip install apache-beam[gcp]
python -m apache_beam.examples.windowed_wordcount --input YOUR_INPUT_FILE \
                                         --output_table PROJECT:DATASET.TABLE \
                                         --runner DataflowRunner \
                                         --project YOUR_GCP_PROJECT \
                                         --temp_location gs://YOUR_GCS_BUCKET/tmp/
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

To view the full code in Python, see
**[windowed_wordcount.py](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/windowed_wordcount.py).**

**To run this example in Go:**

{{< highlight class="runner-direct" >}}
$ go install github.com/apache/beam/sdks/go/examples/windowed_wordcount
$ windowed_wordcount --input <PATH_TO_INPUT_FILE> --output counts
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ go install github.com/apache/beam/sdks/go/examples/windowed_wordcount
# As part of the initial setup, for non linux users - install package unix before run
$ go get -u golang.org/x/sys/unix
$ windowed_wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
            --output gs://<your-gcs-bucket>/counts \
            --runner dataflow \
            --project your-gcp-project \
            --temp_location gs://<your-gcs-bucket>/tmp/ \
            --staging_location gs://<your-gcs-bucket>/binaries/ \
            --worker_harness_container_image=apache-docker-beam-snapshots-docker.bintray.io/beam/go:20180515
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Go SDK.
{{< /highlight >}}

To view the full code in Go, see
**[windowed_wordcount.go](https://github.com/apache/beam/blob/master/sdks/go/examples/windowed_wordcount/windowed_wordcount.go).**


### Unbounded and bounded datasets

Beam allows you to create a single pipeline that can handle both bounded and
unbounded datasets. If your dataset has a fixed number of elements, it is a bounded
dataset and all of the data can be processed together. For bounded datasets,
the question to ask is "Do I have all of the data?" If data continuously
arrives (such as an endless stream of game scores in the
[Mobile gaming example](/get-started/mobile-gaming-example/),
it is an unbounded dataset. An unbounded dataset is never available for
processing at any one time, so the data must be processed using a streaming
pipeline that runs continuously. The dataset will only be complete up to a
certain point, so the question to ask is "Up until what point do I have all of
the data?" Beam uses [windowing](/documentation/programming-guide/#windowing)
to divide a continuously updating dataset into logical windows of finite size.
If your input is unbounded, you must use a runner that supports streaming.

If your pipeline's input is bounded, then all downstream PCollections will also be
bounded. Similarly, if the input is unbounded, then all downstream PCollections
of the pipeline will be unbounded, though separate branches may be independently
bounded.

Recall that the input for this example is a set of Shakespeare's texts, which is
a finite set of data. Therefore, this example reads bounded data from a text
file:

{{< highlight java >}}
public static void main(String[] args) throws IOException {
    Options options = ...
    Pipeline pipeline = Pipeline.create(options);

    PCollection<String> input = pipeline
      .apply(TextIO.read().from(options.getInputFile()))

{{< /highlight >}}

{{< highlight py >}}
def main(arvg=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('--input-file',
                      dest='input_file',
                      default='/Users/home/words-example.txt')
  known_args, pipeline_args = parser.parse_known_args(argv)
  pipeline_options = PipelineOptions(pipeline_args)
  p = beam.Pipeline(options=pipeline_options)
  lines  = p | 'read' >> ReadFromText(known_args.input_file)
{{< /highlight >}}

{{< highlight go >}}
func main() {
   ...
   p := beam.NewPipeline()
   s := p.Root()

   lines := textio.Read(s, *input)
   ...
}
{{< /highlight >}}

### Adding timestamps to data

Each element in a `PCollection` has an associated [timestamp](/documentation/programming-guide#element-timestamps).
The timestamp for each element is initially assigned by the source that creates
the `PCollection`. Some sources that create unbounded PCollections can assign
each new element a timestamp that corresponds to when the element was read or
added. You can manually assign or adjust timestamps with a `DoFn`; however, you
can only move timestamps forward in time.

In this example the input is bounded. For the purpose of the example, the `DoFn`
method named `AddTimestampsFn` (invoked by `ParDo`) will set a timestamp for
each element in the `PCollection`.

{{< highlight java >}}
.apply(ParDo.of(new AddTimestampFn(minTimestamp, maxTimestamp)));
{{< /highlight >}}

{{< highlight py >}}
beam.Map(AddTimestampFn(timestamp_seconds))
{{< /highlight >}}

{{< highlight go >}}
timestampedLines := beam.ParDo(s, &addTimestampFn{Min: mtime.Now()}, lines)
{{< /highlight >}}

Below is the code for `AddTimestampFn`, a `DoFn` invoked by `ParDo`, that sets
the data element of the timestamp given the element itself. For example, if the
elements were log lines, this `ParDo` could parse the time out of the log string
and set it as the element's timestamp. There are no timestamps inherent in the
works of Shakespeare, so in this case we've made up random timestamps just to
illustrate the concept. Each line of the input text will get a random associated
timestamp sometime in a 2-hour period.

{{< highlight java >}}
static class AddTimestampFn extends DoFn<String, String> {
  private final Instant minTimestamp;
  private final Instant maxTimestamp;

  AddTimestampFn(Instant minTimestamp, Instant maxTimestamp) {
    this.minTimestamp = minTimestamp;
    this.maxTimestamp = maxTimestamp;
  }

  @ProcessElement
  public void processElement(ProcessContext c) {
    Instant randomTimestamp =
      new Instant(
          ThreadLocalRandom.current()
          .nextLong(minTimestamp.getMillis(), maxTimestamp.getMillis()));

    /**
     * Concept #2: Set the data element with that timestamp.
     */
    c.outputWithTimestamp(c.element(), new Instant(randomTimestamp));
  }
}
{{< /highlight >}}

{{< highlight py >}}
class AddTimestampFn(beam.DoFn):

  def __init__(self, min_timestamp, max_timestamp):
     self.min_timestamp = min_timestamp
     self.max_timestamp = max_timestamp

  def process(self, element):
    return window.TimestampedValue(
       element,
       random.randint(self.min_timestamp, self.max_timestamp))
{{< /highlight >}}

{{< highlight go >}}
type addTimestampFn struct {
	Min beam.EventTime `json:"min"`
}

func (f *addTimestampFn) ProcessElement(x beam.X) (beam.EventTime, beam.X) {
	timestamp := f.Min.Add(time.Duration(rand.Int63n(2 * time.Hour.Nanoseconds())))
	return timestamp, x
}
{{< /highlight >}}

{{< paragraph class="language-go" >}}
Note that the use of the `beam.X` "type variable" allows the transform to be
used for any type.
{{< /paragraph >}}

### Windowing

Beam uses a concept called **Windowing** to subdivide a `PCollection` into
bounded sets of elements. PTransforms that aggregate multiple elements process
each `PCollection` as a succession of multiple, finite windows, even though the
entire collection itself may be of infinite size (unbounded).

The WindowedWordCount example applies fixed-time windowing, wherein each
window represents a fixed time interval. The fixed window size for this example
defaults to 1 minute (you can change this with a command-line option).

{{< highlight java >}}
PCollection<String> windowedWords = input
  .apply(Window.<String>into(
    FixedWindows.of(Duration.standardMinutes(options.getWindowSize()))));
{{< /highlight >}}

{{< highlight py >}}
windowed_words = input | beam.WindowInto(window.FixedWindows(60 * window_size_minutes))
{{< /highlight >}}

{{< highlight go >}}
windowedLines := beam.WindowInto(s, window.NewFixedWindows(time.Minute), timestampedLines)

{{< /highlight >}}

### Reusing PTransforms over windowed PCollections

You can reuse existing PTransforms that were created for manipulating simple
PCollections over windowed PCollections as well.

{{< highlight java >}}
PCollection<KV<String, Long>> wordCounts = windowedWords.apply(new WordCount.CountWords());
{{< /highlight >}}

{{< highlight py >}}
word_counts = windowed_words | CountWords()
{{< /highlight >}}

{{< highlight go >}}
counted := wordcount.CountWords(s, windowedLines)
{{< /highlight >}}

## StreamingWordCount example

The StreamingWordCount example is a streaming pipeline that reads Pub/Sub
messages from a Pub/Sub subscription or topic, and performs a frequency count on
the words in each message. Similar to WindowedWordCount, this example applies
fixed-time windowing, wherein each window represents a fixed time interval. The
fixed window size for this example is 15 seconds. The pipeline outputs the
frequency count of the words seen in each 15 second window.

**New Concepts:**

* Reading an unbounded dataset
* Writing unbounded results

**To run this example in Java:**

> **Note:** StreamingWordCount is not yet available for the Java SDK.

**To run this example in Python:**

{{< highlight class="runner-direct" >}}
python -m apache_beam.examples.streaming_wordcount \
  --input_topic "projects/YOUR_PUBSUB_PROJECT_NAME/topics/YOUR_INPUT_TOPIC" \
  --output_topic "projects/YOUR_PUBSUB_PROJECT_NAME/topics/YOUR_OUTPUT_TOPIC" \
  --streaming
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
# As part of the initial setup, install Google Cloud Platform specific extra components.
pip install apache-beam[gcp]
python -m apache_beam.examples.streaming_wordcount \
  --runner DataflowRunner \
  --project YOUR_GCP_PROJECT \
  --region YOUR_GCP_REGION \
  --temp_location gs://YOUR_GCS_BUCKET/tmp/ \
  --input_topic "projects/YOUR_PUBSUB_PROJECT_NAME/topics/YOUR_INPUT_TOPIC" \
  --output_topic "projects/YOUR_PUBSUB_PROJECT_NAME/topics/YOUR_OUTPUT_TOPIC" \
  --streaming
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
This runner is not yet available for the Python SDK.
{{< /highlight >}}

To view the full code in Python, see
**[streaming_wordcount.py](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/streaming_wordcount.py).**

**To run this example in Go:**

> **Note:** StreamingWordCount is not yet available for the Go SDK. There is an open issue for this
([BEAM-4292](https://issues.apache.org/jira/browse/BEAM-4292)).


### Reading an unbounded dataset

This example uses an unbounded dataset as input. The code reads Pub/Sub
messages from a Pub/Sub subscription or topic using
[`beam.io.ReadStringsFromPubSub`](https://beam.apache.org/releases/pydoc/{{< param release_latest >}}/apache_beam.io.gcp.pubsub.html#apache_beam.io.gcp.pubsub.ReadStringsFromPubSub).

{{< highlight java >}}
  // This example is not currently available for the Beam SDK for Java.
{{< /highlight >}}

{{< highlight py >}}
  # Read from Pub/Sub into a PCollection.
  if known_args.input_subscription:
    lines = p | beam.io.ReadStringsFromPubSub(
        subscription=known_args.input_subscription)
  else:
    lines = p | beam.io.ReadStringsFromPubSub(topic=known_args.input_topic)
{{< /highlight >}}

{{< highlight go >}}
  // This example is not currently available for the Beam SDK for Go.
{{< /highlight >}}

### Writing unbounded results

When the input is unbounded, the same is true of the output `PCollection`. As
such, you must make sure to choose an appropriate I/O for the results. Some I/Os
support only bounded output, while others support both bounded and unbounded
outputs.

This example uses an unbounded `PCollection` and streams the results to
Google Pub/Sub. The code formats the results and writes them to a Pub/Sub topic
using [`beam.io.WriteStringsToPubSub`](https://beam.apache.org/releases/pydoc/{{< param release_latest >}}/apache_beam.io.gcp.pubsub.html#apache_beam.io.gcp.pubsub.WriteStringsToPubSub).

{{< highlight java >}}
  // This example is not currently available for the Beam SDK for Java.
{{< /highlight >}}

{{< highlight py >}}
  # Write to Pub/Sub
  output | beam.io.WriteStringsToPubSub(known_args.output_topic)
{{< /highlight >}}

{{< highlight go >}}
  // This example is not currently available for the Beam SDK for Go.
{{< /highlight >}}

## Next Steps

* Walk through the Mobile Gaming examples in the [Mobile Gaming Example Walkthrough](/get-started/mobile-gaming-example).
* Take a self-paced tour through our [Learning Resources](/documentation/resources/learning-resources).
* Dive in to some of our favorite [Videos and Podcasts](/documentation/resources/videos-and-podcasts).
* Join the Beam [users@](/community/contact-us) mailing list.

Please don't hesitate to [reach out](/community/contact-us) if you encounter any issues!
