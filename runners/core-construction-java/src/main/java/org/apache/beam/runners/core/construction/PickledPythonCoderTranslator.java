/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.beam.runners.core.construction;

import static org.apache.beam.vendor.guava.v26_0_jre.com.google.common.base.Preconditions.checkArgument;

import org.apache.beam.sdk.coders.Coder;
import org.apache.beam.sdk.coders.PickledPythonCoder;
import org.apache.beam.vendor.guava.v26_0_jre.com.google.common.collect.ImmutableList;

import java.util.List;

public class PickledPythonCoderTranslator implements CoderTranslator<PickledPythonCoder> {
@Override
public List<? extends Coder<?>> getComponents(PickledPythonCoder from) {
    return ImmutableList.of();
    }

@Override
public byte[] getPayload(PickledPythonCoder from) {
    return from.getPayload();
    }

@Override
public PickledPythonCoder fromComponents(List<Coder<?>> components, byte[] payload, CoderTranslation.TranslationContext context) {
    checkArgument(
    components.isEmpty(), "Expected empty component list, but received: " + components);
    return PickledPythonCoder.of(payload);
    }
}
