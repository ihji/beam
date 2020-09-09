---
title: "아파치 빔 해보기"
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

# 아파치 빔 해보기

상호작용 가능한 노트북을 [Colab](https://colab.research.google.com)에 만들어 아파치 빔을 시험해 볼 수 있습니다. 이 노트북을 이용해 여러가지 코드를 실험해보고 코드의 변화가 파이프라인의 실행에 어떤 영향을 미치는지 배웁니다. 노트북을 사용하기 위해 컴퓨터에 어떤 것도 설치할 필요가 없습니다.

{{< language-switcher java py go >}}

## Colab에서 실행하는 단어세기 예제

이 Colab 노트북은 가장 간단한 단어세기 파이프라인 예제를 보여줍니다.

{{< highlight java >}}
package samples.quickstart;

import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.FlatMapElements;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.values.TypeDescriptors;

import java.util.Arrays;

public class WordCount {
  public static void main(String[] args) {
    String inputsDir = "data/*";
    String outputsPrefix = "outputs/part";

    PipelineOptions options = PipelineOptionsFactory.fromArgs(args).create();
    Pipeline pipeline = Pipeline.create(options);
    pipeline
        .apply("Read lines", TextIO.read().from(inputsDir))
        .apply("Find words", FlatMapElements.into(TypeDescriptors.strings())
            .via((String line) -> Arrays.asList(line.split("[^\\p{L}]+"))))
        .apply("Filter empty words", Filter.by((String word) -> !word.isEmpty()))
        .apply("Count words", Count.perElement())
        .apply("Write results", MapElements.into(TypeDescriptors.strings())
            .via((KV<String, Long> wordCount) ->
                  wordCount.getKey() + ": " + wordCount.getValue()))
        .apply(TextIO.write().to(outputsPrefix));
    pipeline.run();
  }
}
{{< /highlight >}}

{{< paragraph class="language-java" >}}
<a class="button button--primary" target="_blank"
  href="https://colab.sandbox.google.com/github/{{< param branch_repo >}}/examples/notebooks/get-started/try-apache-beam-java.ipynb">
  Colab에서 실행
</a>
<a class="button button--primary" target="_blank"
  href="https://github.com/{{< param branch_repo >}}/examples/notebooks/get-started/try-apache-beam-java.ipynb">
  GitHub에서 보기
</a>
{{< /paragraph >}}

{{< paragraph class="language-java" >}}
아파치 빔 자바 개발 도구를 컴퓨터에 직접 설치하고 실행하기 위해서는 <a href="/ko/get-started/quickstart-java">자바 빠르게 시작하기</a> 문서를 참고하세요.
{{< /paragraph >}}

{{< highlight py >}}
import apache_beam as beam
import re

inputs_pattern = 'data/*'
outputs_prefix = 'outputs/part'

with beam.Pipeline() as pipeline:
  (
      pipeline
      | 'Read lines' >> beam.io.ReadFromText(inputs_pattern)
      | 'Find words' >> beam.FlatMap(lambda line: re.findall(r"[a-zA-Z']+", line))
      | 'Pair words with 1' >> beam.Map(lambda word: (word, 1))
      | 'Group and sum' >> beam.CombinePerKey(sum)
      | 'Format results' >> beam.Map(lambda word_count: str(word_count))
      | 'Write results' >> beam.io.WriteToText(outputs_prefix)
  )
{{< /highlight >}}

{{< paragraph class="language-py" >}}
<a class="button button--primary" target="_blank"
  href="https://colab.sandbox.google.com/github/{{< param branch_repo >}}/examples/notebooks/get-started/try-apache-beam-py.ipynb">
  Colab에서 실행
</a>
<a class="button button--primary" target="_blank"
  href="https://github.com/{{< param branch_repo >}}/examples/notebooks/get-started/try-apache-beam-py.ipynb">
  GitHub에서 보기
</a>
{{< /paragraph >}}

{{< paragraph class="language-py" >}}
아파치 빔 파이썬 개발 도구를 컴퓨터에 직접 설치하고 실행하기 위해서는 <a href="/ko/get-started/quickstart-py">파이썬 빠르게 시작하기</a> 문서를 참고하세요.
{{< /paragraph >}}

{{< highlight go >}}
package main

import (
	"context"
	"flag"
	"fmt"
	"regexp"

	"github.com/apache/beam/sdks/go/pkg/beam"
	"github.com/apache/beam/sdks/go/pkg/beam/io/textio"
	"github.com/apache/beam/sdks/go/pkg/beam/runners/direct"
	"github.com/apache/beam/sdks/go/pkg/beam/transforms/stats"

	_ "github.com/apache/beam/sdks/go/pkg/beam/io/filesystem/local"
)

var (
	input = flag.String("input", "data/*", "File(s) to read.")
	output = flag.String("output", "outputs/wordcounts.txt", "Output filename.")
)

var wordRE = regexp.MustCompile(`[a-zA-Z]+('[a-z])?`)

func main() {
  flag.Parse()

	beam.Init()

	pipeline := beam.NewPipeline()
	root := pipeline.Root()

	lines := textio.Read(root, *input)
	words := beam.ParDo(root, func(line string, emit func(string)) {
		for _, word := range wordRE.FindAllString(line, -1) {
			emit(word)
		}
	}, lines)
	counted := stats.Count(root, words)
	formatted := beam.ParDo(root, func(word string, count int) string {
		return fmt.Sprintf("%s: %v", word, count)
	}, counted)
	textio.Write(root, *output, formatted)

	direct.Execute(context.Background(), pipeline)
}
{{< /highlight >}}

{{< paragraph class="language-go" >}}
<a class="button button--primary" target="_blank"
  href="https://colab.sandbox.google.com/github/{{< param branch_repo >}}/examples/notebooks/get-started/try-apache-beam-go.ipynb">
  Colab에서 실행
</a>
<a class="button button--primary" target="_blank"
  href="https://github.com/{{< param branch_repo >}}/examples/notebooks/get-started/try-apache-beam-go.ipynb">
  GitHub에서 보기
</a>
{{< /paragraph >}}

{{< paragraph class="language-go" >}}
아파치 빔 고 개발도구를 컴퓨터에 직접 설치하고 실행하기 위해서는 <a href="/ko/get-started/quickstart-go">고 빠르게 시작하기</a> 문서를 참고하세요.
{{< /paragraph >}}

단어세기 파이프라인의 자세한 동작에 대한 설명은 [단어세기 예제 따라잡기](/ko/get-started/wordcount-example)에서 볼 수 있습니다.

## 다음 할일들

* [단어세기 예제 따라잡기](/ko/get-started/wordcount-example)에서 추가적인 단어세기 예제들을 찾아봅니다.
* [학습 자료](/ko/documentation/resources/learning-resources)를 통해 자습에 필요한 정보를 얻습니다.
* 재미있는 [비디오와 팟캐스트](/ko/documentation/resources/videos-and-podcasts)들을 시청합니다.
* 빔 유저([users@](/ko/community/contact-us)) 메일링 리스트에 참여합니다.
* 아파치 빔 코드에 기여하는 것에 관심이 있다면 [기여하기 가이드](/ko/contribute)를 읽어보세요.

아파치 빔을 사용하다 문제에 맞닥뜨렸다면 주저하지 말고 [연락](/ko/community/contact-us) 주세요!
