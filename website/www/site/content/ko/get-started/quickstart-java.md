---
title: "빔 자바 빠르게 시작하기"
aliases:
  - /get-started/quickstart/
  - /use/quickstart/
  - /getting-started/
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

# 아파치 빔 자바 개발 도구 빠르게 시작하기

이 빠르게 시작하기 문서는 독자가 [단어세기](/ko/get-started/wordcount-example)를 실행하는 빔 파이프라인을 처음으로 실행할 수 있도록 돕습니다. 파이프라인은 빔의 [자바 개발 도구](/ko/documentation/sdks/java)를 이용하여 작성되며 독자가 고른 [실행기](/ko/documentation#runners) 위에서 동작합니다.

아파치 빔 자바 개발 도구의 개발에 기여하고 싶으시다면 [기여하기 가이드](/ko/contribute)를 읽어보세요!

{{< toc >}}

## 개발 환경 구성하기

1. [자바 개발 도구 (JDK)](https://www.oracle.com/technetwork/java/javase/downloads/index.html) version 8을 다운로드 하고 설치합니다. [JAVA_HOME](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/envvars001.html) 환경 변수가 JDK 설치 경로를 제대로 가리키고 있는지 확인 합니다.

1. 운영체제에 맞는 메이븐의 [설치 가이드](https://maven.apache.org/install.html)를 참고하여 [아파치 메이븐](https://maven.apache.org/download.cgi)을 다운로드 하고 설치합니다.

1. 선택사항: 메이븐 프로젝트를 그레이들 프로젝트로 변환하고 싶다면 [그레이들](https://gradle.org/install/)을 설치합니다.

## 단어세기 예제 코드 구하기

단어세기 예제 코드의 복사본을 구하는 가장 쉬운 방법은 아래 명령어를 이용하여 간단한 메이븐 프로젝트를 생성하는 것입니다. 생성된 프로젝트는 가장 최신의 빔 릴리즈에서 컴파일 되는 빔의 WordCount 예제 클래스를 포함하고 있습니다:

{{< highlight class="shell-unix" >}}
$ mvn archetype:generate \
      -DarchetypeGroupId=org.apache.beam \
      -DarchetypeArtifactId=beam-sdks-java-maven-archetypes-examples \
      -DarchetypeVersion={{< param release_latest >}} \
      -DgroupId=org.example \
      -DartifactId=word-count-beam \
      -Dversion="0.1" \
      -Dpackage=org.apache.beam.examples \
      -DinteractiveMode=false
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> mvn archetype:generate `
 -D archetypeGroupId=org.apache.beam `
 -D archetypeArtifactId=beam-sdks-java-maven-archetypes-examples `
 -D archetypeVersion={{< param release_latest >}} `
 -D groupId=org.example `
 -D artifactId=word-count-beam `
 -D version="0.1" `
 -D package=org.apache.beam.examples `
 -D interactiveMode=false
{{< /highlight >}}

이 명령어는 기본적인 `pom.xml` 빌드 파일과 텍스트 파일 안의 단어 수를 세는 예제 파이프라인을 포함한 `word-count-beam` 디렉토리를 생성합니다.

{{< highlight class="shell-unix" >}}
$ cd word-count-beam/

$ ls
pom.xml	src

$ ls src/main/java/org/apache/beam/examples/
DebuggingWordCount.java	WindowedWordCount.java	common
MinimalWordCount.java	WordCount.java
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> cd .\word-count-beam

PS> dir

...

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/19/2018  11:00 PM                src
-a----        7/19/2018  11:00 PM          16051 pom.xml

PS> dir .\src\main\java\org\apache\beam\examples

...
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/19/2018  11:00 PM                common
d-----        7/19/2018  11:00 PM                complete
d-----        7/19/2018  11:00 PM                subprocess
-a----        7/19/2018  11:00 PM           7073 DebuggingWordCount.java
-a----        7/19/2018  11:00 PM           5945 MinimalWordCount.java
-a----        7/19/2018  11:00 PM           9490 WindowedWordCount.java
-a----        7/19/2018  11:00 PM           7662 WordCount.java
{{< /highlight >}}

이 예제에서 사용된 빔의 여러 개념들에 대한 자세한 설명은 [단어세기 예제 따라잡기](/ko/get-started/wordcount-example) 문서를 참고하세요. 여기서는 우선 `WordCount.java`를 실행하는 것에만 집중 하겠습니다.

## 선택사항: 메이븐을 그레이들 프로젝트로 변환하기

방금 전 실행한 명령어를 통해 생성된 `pom.xml` 파일이 있는 디렉토리로 이동합니다. 다음 명령어를 실행하여 메이븐 프로젝트를 그레이들 프로젝트로 변환합니다:
{{< highlight >}}
$ gradle init
{{< /highlight >}}

그레이들 프로젝트로의 변환이 끝나고 나면:

1. 생성된 `build.gradle` 파일을 수정하여 `repositories` 아래에 `mavenCentral()`을 추가합니다:
{{< highlight >}}
repositories {
    mavenCentral()
    maven {
        url = uri('https://repository.apache.org/content/repositories/snapshots/')
    }

    maven {
        url = uri('http://repo.maven.apache.org/maven2')
    }
}
{{< /highlight >}}
1. 다음 작업을 `build.gradle`에 추가하여 그레이들을 통해 파이프라인을 실행할 수 있도록 만듭니다:
{{< highlight >}}
task execute (type:JavaExec) {
    main = System.getProperty("mainClass")
    classpath = sourceSets.main.runtimeClasspath
    systemProperties System.getProperties()
    args System.getProperty("exec.args", "").split()
}
{{< /highlight >}}
1. 다음을 실행하여 프로젝트를 다시 빌드합니다:
{{< highlight >}}
$ gradle build
{{< /highlight >}}

## 단어세기 실행하기

동일한 빔 파이프라인을 다양한 빔 [실행기](/ko/documentation#runners)에서 실행 할 수 있습니다. 대표적인 실행기로는 [FlinkRunner](/ko/documentation/runners/flink), [SparkRunner](/ko/documentation/runners/spark), [NemoRunner](/ko/documentation/runners/nemo), [JetRunner](/ko/documentation/runners/jet), 또는 [DataflowRunner](/ko/documentation/runners/dataflow) 등이 있습니다. 로컬 머신에서 실행 되고 특별한 설정이 필요 없는 [DirectRunner](/documentation/runners/direct)는 아파치 빔을 처음 시작하기에 적합 합니다.

사용하기 원하는 실행기를 선택하고 나면:

1.  특정 실행기를 위한 환경 설정이 마무리 되었는지 확인합니다.
1.  다음을 참고하여 실행 명령어를 작성합니다:
    1. `--runner=<runner>` 옵션을 지정하여 특정 실행기를 선택합니다. (기본값은 [DirectRunner](/ko/documentation/runners/direct)입니다.)
    1. 지정한 실행기가 요구하는 옵션을 추가합니다.
    1. 입력 파일과 출력 위치를 선택합니다. 선택한 파일과 위치는 지정된 실행기에서 접근 가능해야 합니다. (예를 들어 파이프라인을 외부 클러스터에서 실행한다면 로컬 파일에 접근하는 것은 불가능합니다.)
1.  단어세기 파이프라인을 실행해 봅니다.

### 메이븐으로 단어세기 실행하기

유닉스 쉘에서:

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

플링크 대쉬보드(http://<flink master>:8081)를 열어 실행중인 작업을 모니터 할 수 있습니다.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--runner=SparkRunner --inputFile=pom.xml --output=counts" -Pspark-runner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
실행하기 전에 /ko/documentation/runners/dataflow/#setup 을 참고하여 필요한 설정이 완료되었는지 확인하세요.

$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--runner=DataflowRunner --project=<your-gcp-project> \
                  --region=<your-gcp-region> \
                  --gcpTempLocation=gs://<your-gcs-bucket>/tmp \
                  --inputFile=gs://apache-beam-samples/shakespeare/* --output=gs://<your-gcs-bucket>/counts" \
     -Pdataflow-runner
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
$ mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--inputFile=pom.xml --output=/tmp/counts --runner=SamzaRunner" -Psamza-runner
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
$ mvn package -Pnemo-runner && java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WordCount \
     --runner=NemoRunner --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
$ mvn package -Pjet-runner
$ java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WordCount \
     --runner=JetRunner --jetLocalMode=3 --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

윈도우즈 파워쉘에서:

{{< highlight class="runner-direct" >}}
PS> mvn compile exec:java -D exec.mainClass=org.apache.beam.examples.WordCount `
 -D exec.args="--inputFile=pom.xml --output=counts" -P direct-runner
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
PS> mvn compile exec:java -D exec.mainClass=org.apache.beam.examples.WordCount `
 -D exec.args="--runner=FlinkRunner --inputFile=pom.xml --output=counts" -P flink-runner
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
PS> mvn package exec:java -D exec.mainClass=org.apache.beam.examples.WordCount `
 -D exec.args="--runner=FlinkRunner --flinkMaster=<flink master> --filesToStage=.\target\word-count-beam-bundled-0.1.jar `
               --inputFile=C:\path\to\quickstart\pom.xml --output=C:\tmp\counts" -P flink-runner

플링크 대쉬보드(http://<flink master>:8081)를 열어 실행중인 작업을 모니터 할 수 있습니다.
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
PS> mvn compile exec:java -D exec.mainClass=org.apache.beam.examples.WordCount `
 -D exec.args="--runner=SparkRunner --inputFile=pom.xml --output=counts" -P spark-runner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
실행하기 전에 /ko/documentation/runners/dataflow/#setup 을 참고하여 필요한 설정이 완료되었는지 확인하세요.

PS> mvn compile exec:java -D exec.mainClass=org.apache.beam.examples.WordCount `
 -D exec.args="--runner=DataflowRunner --project=<your-gcp-project> `
               --region=<your-gcp-region> \
               --gcpTempLocation=gs://<your-gcs-bucket>/tmp `
               --inputFile=gs://apache-beam-samples/shakespeare/* --output=gs://<your-gcs-bucket>/counts" `
 -P dataflow-runner
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
PS> mvn compile exec:java -D exec.mainClass=org.apache.beam.examples.WordCount `
     -D exec.args="--inputFile=pom.xml --output=/tmp/counts --runner=SamzaRunner" -P samza-runner
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
PS> mvn package -P nemo-runner -DskipTests
PS> java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WordCount `
      --runner=NemoRunner --inputFile=`pwd`/pom.xml --output=counts
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
PS> mvn package -P jet-runner
PS> java -cp target/word-count-beam-bundled-0.1.jar org.apache.beam.examples.WordCount `
      --runner=JetRunner --jetLocalMode=3 --inputFile=$pwd/pom.xml --output=counts
{{< /highlight >}}

### 그레이들로 단어세기 실행하기

유닉스 쉘에서 (현재 Direct, Spark, 그리고 Dataflow 실행기에 대한 예제만 제공됩니다):

{{< highlight class="runner-direct">}}
$ gradle clean execute -DmainClass=org.apache.beam.examples.WordCount \
    -Dexec.args="--inputFile=pom.xml --output=counts" -Pdirect-runner
{{< /highlight >}}

{{< highlight class="runner-apex">}}
이 실행기에 대한 예제를 추가하고 있습니다!
{{< /highlight >}}

{{< highlight class="runner-flink-local">}}
이 실행기에 대한 예제를 추가하고 있습니다!
{{< /highlight >}}

{{< highlight class="runner-flink-cluster">}}
이 실행기에 대한 예제를 추가하고 있습니다!
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ gradle clean execute -DmainClass=org.apache.beam.examples.WordCount \
    -Dexec.args="--inputFile=pom.xml --output=counts" -Pspark-runner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ gradle clean execute -DmainClass=org.apache.beam.examples.WordCount \
    -Dexec.args="--project=<your-gcp-project> --inputFile=gs://apache-beam-samples/shakespeare/* \
    --output=gs://<your-gcs-bucket>/counts" -Pdataflow-runner
{{< /highlight >}}

{{< highlight class="runner-samza-local">}}
이 실행기에 대한 예제를 추가하고 있습니다!
{{< /highlight >}}

{{< highlight class="runner-nemo">}}
이 실행기에 대한 예제를 추가하고 있습니다!
{{< /highlight >}}

{{< highlight class="runner-jet">}}
이 실행기에 대한 예제를 추가하고 있습니다!
{{< /highlight >}}

## 결과 확인하기

파이프라인 실행이 완료되고 나면 결과를 볼 수 있습니다. 출력 파일은 여러개로 생성되며 모두 `count`로 시작하는 이름을 가지고 있습니다. 정확한 출력 파일 개수는 실행기에 의해 결정되며 이는 효과적인 분산처리를 위하여 의도적으로 실행기에게 위임된 매개변수 입니다.

{{< highlight class="runner-direct" >}}
$ ls counts*
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
$ ls counts*
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
$ ls /tmp/counts*
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ ls counts*
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ gsutil ls gs://<your-gcs-bucket>/counts*
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
$ ls /tmp/counts*
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
$ ls counts*
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
$ ls counts*
{{< /highlight >}}

파일의 내용을 들여다보면 중복이 없는 단어들의 목록과 각각의 단어가 몇번이나 등장했는지를 나타내는 숫자를 찾을 수 있습니다. 파일 내에 등장하는 단어들의 순서는 아래 표시된 예제와 다를 수 있는데 이는 빔 모델이 데이터의 순서를 보장하지 않기 때문입니다. 역시 효과적인 분산처리를 위하여 실행기에게 주어진 자유입니다.

{{< highlight class="runner-direct" >}}
$ more counts*
api: 9
bundled: 1
old: 4
Apache: 2
The: 1
limitations: 1
Foundation: 1
...
{{< /highlight >}}

{{< highlight class="runner-flink-local" >}}
$ more counts*
The: 1
api: 9
old: 4
Apache: 2
limitations: 1
bundled: 1
Foundation: 1
...
{{< /highlight >}}

{{< highlight class="runner-flink-cluster" >}}
$ more /tmp/counts*
The: 1
api: 9
old: 4
Apache: 2
limitations: 1
bundled: 1
Foundation: 1
...
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
$ more counts*
beam: 27
SF: 1
fat: 1
job: 1
limitations: 1
require: 1
of: 11
profile: 10
...
{{< /highlight >}}


{{< highlight class="runner-dataflow" >}}
$ gsutil cat gs://<your-gcs-bucket>/counts*
feature: 15
smother'st: 1
revelry: 1
bashfulness: 1
Bashful: 1
Below: 2
deserves: 32
barrenly: 1
...
{{< /highlight >}}

{{< highlight class="runner-samza-local" >}}
$ more /tmp/counts*
api: 7
are: 2
can: 2
com: 14
end: 14
for: 14
has: 2
...
{{< /highlight >}}

{{< highlight class="runner-nemo" >}}
$ more counts*
cluster: 2
handler: 1
plugins: 9
exclusions: 14
finalName: 2
Adds: 2
java: 7
xml: 1
...
{{< /highlight >}}

{{< highlight class="runner-jet" >}}
$ more counts*
FlinkRunner: 1
cleanupDaemonThreads: 2
sdks: 4
unit: 1
Apache: 3
IO: 2
copyright: 1
governing: 1
overrides: 1
YARN: 1
...
{{< /highlight >}}

## 다음 할일들

* [빔 자바 개발 도구](/ko/documentation/sdks/java/)에 대하여 더 알아보고 [자바 개발 도구 API 사전](https://beam.apache.org/releases/javadoc)을 훑어 봅니다.
* [단어세기 예제 따라잡기](/ko/get-started/wordcount-example)를 통해 단어세기 예제에 대하여 알아봅니다.
* [학습 자료](/ko/documentation/resources/learning-resources)를 통해 자습에 필요한 정보를 얻습니다.
* 재미있는 [비디오와 팟캐스트](/ko/documentation/resources/videos-and-podcasts)들을 시청합니다.
* 빔 유저([users@](/ko/community/contact-us)) 메일링 리스트에 참여합니다.

아파치 빔을 사용하다 문제에 맞닥뜨렸다면 주저하지 말고 [연락](/ko/community/contact-us) 주세요!
