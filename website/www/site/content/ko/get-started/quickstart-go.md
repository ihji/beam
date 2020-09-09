---
title: "빔 고 빠르게 시작하기"
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

# 아파치 빔 고 개발 도구 빠르게 시작하기

이 빠르게 시작하기 문서는 독자가 [단어세기](/ko/get-started/wordcount-example)를 실행하는 빔 파이프라인을 처음으로 실행할 수 있도록 돕습니다. 파이프라인은 빔의 [고 개발 도구](/ko/documentation/sdks/go)를 이용하여 작성되며 독자가 고른 [실행기](/ko/documentation#runners) 위에서 동작합니다.

아파치 빔 고 개발 도구의 개발에 기여하고 싶으시다면 [기여하기 가이드](/ko/contribute)를 읽어보세요!

{{< toc >}}

## 환경 설정하기

빔 고 개발 도구는 `go` 버전 1.10 이상을 필요로 합니다. [여기](https://golang.org/)서 다운로드 할 수 있습니다. 버전이 1.10 이상인지 확인하기 위해 다음을 실행합니다:

{{< highlight >}}
$ go version
{{< /highlight >}}

## 개발 도구와 예제 설치하기

아파치 빔 고 개발 도구를 설치하는 가장 쉬운 방법은 `go get` 명령어를 이용하는 것입니다:

{{< highlight >}}
$ go get -u github.com/apache/beam/sdks/go/...
{{< /highlight >}}

고 개발 도구 개발에 대한 정보는 [BUILD.md](https://github.com/apache/beam/blob/master/sdks/go/BUILD.md)을 확인하세요.

## 단어세기 실행하기

아파치 빔의 [examples](https://github.com/apache/beam/tree/master/sdks/go/examples) 디렉토리는 많은 예제들을 포함하고 있습니다. 모든 예제는 파일 안에 설명된 필수 옵션을 지정하여 실행해 볼 수 있습니다.

예를 들어 `wordcount`는 다음 명령어로 실행합니다:

{{< highlight class="runner-direct" >}}
$ go install github.com/apache/beam/sdks/go/examples/wordcount
$ wordcount --input <PATH_TO_INPUT_FILE> --output counts
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
$ go install github.com/apache/beam/sdks/go/examples/wordcount
# 리눅스 사용자가 아닌 경우 실행하기 전 unix 패키지를 추가로 설치해 주세요
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

## 다음 할일들

* [빔 고 개발 도구](/ko/documentation/sdks/go/)에 대하여 더 알아보고 [godoc](https://godoc.org/github.com/apache/beam/sdks/go/pkg/beam)을 훑어 봅니다.
* [단어세기 예제 따라잡기](/ko/get-started/wordcount-example)를 통해 단어세기 예제에 대하여 알아봅니다.
* [학습 자료](/ko/documentation/resources/learning-resources)를 통해 자습에 필요한 정보를 얻습니다.
* 재미있는 [비디오와 팟캐스트](/ko/documentation/resources/videos-and-podcasts)들을 시청합니다.
* 빔 유저([users@](/ko/community/contact-us)) 메일링 리스트에 참여합니다.

아파치 빔을 사용하다 문제에 맞닥뜨렸다면 주저하지 말고 [연락](/ko/community/contact-us) 주세요!
